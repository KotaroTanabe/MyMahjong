import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Tile, calculateScore } from '../src/index.js';

test('tanyao detection and scoring', () => {
  const hand = Array.from({ length: 14 }, () => new Tile({ suit: 'man', value: 2 }));
  const result = calculateScore(hand);
  assert.deepStrictEqual(result, { yaku: ['tanyao'], han: 1, fu: 20, points: 20 });
});

test('chiitoitsu detection and scoring', () => {
  const pairs = [1,2,3,4,5,6,7];
  const hand = pairs.flatMap(v => [
    new Tile({ suit: 'man', value: v as 1|2|3|4|5|6|7|8|9 }),
    new Tile({ suit: 'man', value: v as 1|2|3|4|5|6|7|8|9 }),
  ]);
  const result = calculateScore(hand);
  assert.ok(result.yaku.includes('chiitoitsu'));
  assert.strictEqual(result.han, 2);
  assert.strictEqual(result.points, 40);
});

test('hand with honors scores zero', () => {
  const hand = [
    new Tile({ suit: 'wind', value: 'east' }),
    ...Array.from({ length: 13 }, () => new Tile({ suit: 'man', value: 2 })),
  ];
  const result = calculateScore(hand);
  assert.strictEqual(result.han, 0);
  assert.strictEqual(result.points, 0);
});

test('yakuhai detection for dragon triplet', () => {
  const hand = [
    new Tile({ suit: 'dragon', value: 'white' }),
    new Tile({ suit: 'dragon', value: 'white' }),
    new Tile({ suit: 'dragon', value: 'white' }),
    ...Array.from({ length: 11 }, () => new Tile({ suit: 'man', value: 2 })),
  ];
  const result = calculateScore(hand);
  assert.ok(result.yaku.includes('yakuhai-white'));
  assert.strictEqual(result.han, 1);
  assert.strictEqual(result.points, 20);
});

test('multiple yakuhai triplets each add han', () => {
  const hand = [
    // dragon triplet
    new Tile({ suit: 'dragon', value: 'green' }),
    new Tile({ suit: 'dragon', value: 'green' }),
    new Tile({ suit: 'dragon', value: 'green' }),
    // wind triplet
    new Tile({ suit: 'wind', value: 'east' }),
    new Tile({ suit: 'wind', value: 'east' }),
    new Tile({ suit: 'wind', value: 'east' }),
    // rest of hand
    ...Array.from({ length: 8 }, () => new Tile({ suit: 'man', value: 2 })),
  ];
  const result = calculateScore(hand);
  assert.ok(result.yaku.includes('yakuhai-green'));
  assert.ok(result.yaku.includes('yakuhai-east'));
  assert.strictEqual(result.han, 2);
  assert.strictEqual(result.points, 40);
});
