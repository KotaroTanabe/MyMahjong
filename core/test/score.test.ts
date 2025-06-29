import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Tile, calculateScore } from '../src/index.js';

test('tanyao detection and scoring', () => {
  const hand = [
    new Tile({ suit: 'man', value: 2 }),
    new Tile({ suit: 'man', value: 3 }),
    new Tile({ suit: 'man', value: 4 }),
    new Tile({ suit: 'pin', value: 2 }),
    new Tile({ suit: 'pin', value: 3 }),
    new Tile({ suit: 'pin', value: 4 }),
    new Tile({ suit: 'sou', value: 2 }),
    new Tile({ suit: 'sou', value: 3 }),
    new Tile({ suit: 'sou', value: 4 }),
    new Tile({ suit: 'man', value: 5 }),
    new Tile({ suit: 'man', value: 6 }),
    new Tile({ suit: 'man', value: 7 }),
    new Tile({ suit: 'pin', value: 6 }),
    new Tile({ suit: 'pin', value: 6 }),
  ];
  const result = calculateScore(hand);
  assert.deepStrictEqual(result.yaku, ['tanyao']);
  assert.strictEqual(result.han, 1);
  assert.strictEqual(result.fu, 20);
  assert.strictEqual(result.points, 700);
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
  assert.strictEqual(result.points, 1300);
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
    // sequences
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 2 }),
    new Tile({ suit: 'man', value: 3 }),
    new Tile({ suit: 'man', value: 4 }),
    new Tile({ suit: 'man', value: 5 }),
    new Tile({ suit: 'man', value: 6 }),
    new Tile({ suit: 'man', value: 7 }),
    new Tile({ suit: 'man', value: 8 }),
    new Tile({ suit: 'man', value: 9 }),
    // dragon triplet
    new Tile({ suit: 'dragon', value: 'white' }),
    new Tile({ suit: 'dragon', value: 'white' }),
    new Tile({ suit: 'dragon', value: 'white' }),
    // pair
    new Tile({ suit: 'pin', value: 2 }),
    new Tile({ suit: 'pin', value: 2 }),
  ];
  const result = calculateScore(hand);
  assert.ok(result.yaku.includes('yakuhai-white'));
  assert.strictEqual(result.han, 1);
  assert.strictEqual(result.rawFu, 24);
  assert.strictEqual(result.fu, 30);
  assert.strictEqual(result.points, 1000);
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
    // sequences
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 2 }),
    new Tile({ suit: 'man', value: 3 }),
    new Tile({ suit: 'man', value: 4 }),
    new Tile({ suit: 'man', value: 5 }),
    new Tile({ suit: 'man', value: 6 }),
    // pair
    new Tile({ suit: 'pin', value: 2 }),
    new Tile({ suit: 'pin', value: 2 }),
  ];
  const result = calculateScore(hand);
  assert.ok(result.yaku.includes('yakuhai-green'));
  assert.ok(result.yaku.includes('yakuhai-east'));
  assert.strictEqual(result.han, 2);
  assert.strictEqual(result.rawFu, 28);
  assert.strictEqual(result.fu, 30);
  assert.strictEqual(result.points, 2000);
});

test('toitoi detection and fu calculation', () => {
  const hand = [
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 2 }),
    new Tile({ suit: 'man', value: 2 }),
    new Tile({ suit: 'man', value: 2 }),
    new Tile({ suit: 'man', value: 3 }),
    new Tile({ suit: 'man', value: 3 }),
    new Tile({ suit: 'man', value: 3 }),
    new Tile({ suit: 'dragon', value: 'red' }),
    new Tile({ suit: 'dragon', value: 'red' }),
    new Tile({ suit: 'dragon', value: 'red' }),
    new Tile({ suit: 'wind', value: 'east' }),
    new Tile({ suit: 'wind', value: 'east' }),
  ];
  const result = calculateScore(hand);
  assert.ok(result.yaku.includes('toitoi'));
  assert.ok(result.yaku.includes('yakuhai-red'));
  assert.strictEqual(result.han, 3);
  // pair of east winds adds fu, plus three simple triplets and one honor triplet
  assert.strictEqual(result.rawFu, 32);
  assert.strictEqual(result.fu, 40);
  assert.strictEqual(result.points, 5200);
});

test('iipeikou detection and scoring', () => {
  const hand = [
    // identical sequences
    new Tile({ suit: 'man', value: 2 }),
    new Tile({ suit: 'man', value: 3 }),
    new Tile({ suit: 'man', value: 4 }),
    new Tile({ suit: 'man', value: 2 }),
    new Tile({ suit: 'man', value: 3 }),
    new Tile({ suit: 'man', value: 4 }),
    // additional sequences
    new Tile({ suit: 'pin', value: 3 }),
    new Tile({ suit: 'pin', value: 4 }),
    new Tile({ suit: 'pin', value: 5 }),
    new Tile({ suit: 'sou', value: 7 }),
    new Tile({ suit: 'sou', value: 8 }),
    new Tile({ suit: 'sou', value: 9 }),
    // pair
    new Tile({ suit: 'dragon', value: 'green' }),
    new Tile({ suit: 'dragon', value: 'green' }),
  ];
  const result = calculateScore(hand);
  assert.ok(result.yaku.includes('iipeikou'));
  assert.strictEqual(result.han, 1);
  assert.strictEqual(result.fu, 30);
  assert.strictEqual(result.points, 1000);
});
