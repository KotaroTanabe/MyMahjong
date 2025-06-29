import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Tile, analyzeHand } from '../src/index.js';

function standardWinningHand(): Tile[] {
  return [
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 2 }),
    new Tile({ suit: 'man', value: 3 }),
    new Tile({ suit: 'man', value: 4 }),
    new Tile({ suit: 'man', value: 5 }),
    new Tile({ suit: 'man', value: 6 }),
    new Tile({ suit: 'man', value: 7 }),
    new Tile({ suit: 'man', value: 8 }),
    new Tile({ suit: 'man', value: 9 }),
    new Tile({ suit: 'pin', value: 1 }),
    new Tile({ suit: 'pin', value: 1 }),
    new Tile({ suit: 'pin', value: 1 }),
    new Tile({ suit: 'pin', value: 2 }),
    new Tile({ suit: 'pin', value: 2 })
  ];
}

test('analyzeHand parses standard winning hand', () => {
  const hand = standardWinningHand();
  const result = analyzeHand(hand);
  assert.ok(result);
  assert.strictEqual(result!.pair[0].toString(), 'pin-2');
  assert.strictEqual(result!.pair[1].toString(), 'pin-2');
  assert.strictEqual(result!.melds.length, 4);
  const meldStrings = result!.melds.map(m => m.tiles.map(t => t.toString()).join(','));
  assert.ok(meldStrings.includes('man-1,man-2,man-3'));
  assert.ok(meldStrings.includes('man-4,man-5,man-6'));
  assert.ok(meldStrings.includes('man-7,man-8,man-9'));
  assert.ok(meldStrings.includes('pin-1,pin-1,pin-1'));
});

function mixedHand(): Tile[] {
  return [
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'pin', value: 2 }),
    new Tile({ suit: 'pin', value: 2 }),
    new Tile({ suit: 'pin', value: 2 }),
    new Tile({ suit: 'sou', value: 3 }),
    new Tile({ suit: 'sou', value: 4 }),
    new Tile({ suit: 'sou', value: 5 }),
    new Tile({ suit: 'sou', value: 6 }),
    new Tile({ suit: 'sou', value: 7 }),
    new Tile({ suit: 'sou', value: 8 }),
    new Tile({ suit: 'dragon', value: 'white' }),
    new Tile({ suit: 'dragon', value: 'white' })
  ];
}

test('analyzeHand handles mix of sequences and triplets', () => {
  const hand = mixedHand();
  const result = analyzeHand(hand);
  assert.ok(result);
  assert.strictEqual(result!.pair[0].toString(), 'dragon-white');
  assert.strictEqual(result!.melds.length, 4);
  const types = result!.melds.map(m => m.type);
  assert.strictEqual(types.filter(t => t === 'triplet').length, 2);
  assert.strictEqual(types.filter(t => t === 'sequence').length, 2);
});
