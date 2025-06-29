import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Tile, Game, Wall, isWinningHand } from '../src/index.js';

function standardWinningHand(): Tile[] {
  return [
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
    // triplet
    new Tile({ suit: 'pin', value: 1 }),
    new Tile({ suit: 'pin', value: 1 }),
    new Tile({ suit: 'pin', value: 1 }),
    // pair
    new Tile({ suit: 'pin', value: 2 }),
    new Tile({ suit: 'pin', value: 2 })
  ];
}

test('detects standard winning hand', () => {
  const hand = standardWinningHand();
  assert.ok(isWinningHand(hand));
});

test('game reports winning hand', () => {
  const hand = standardWinningHand();
  const game = new Game(1, new Wall([]));
  game.players[0].hand.push(...hand);
  assert.ok(game.isWinningHand(0));
});

test('non-winning hand returns false', () => {
  const hand = [
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 2 }),
    new Tile({ suit: 'man', value: 2 }),
    new Tile({ suit: 'man', value: 3 }),
    new Tile({ suit: 'man', value: 3 }),
    new Tile({ suit: 'man', value: 4 }),
    new Tile({ suit: 'man', value: 5 }),
    new Tile({ suit: 'man', value: 6 }),
    new Tile({ suit: 'man', value: 7 }),
    new Tile({ suit: 'man', value: 8 }),
    new Tile({ suit: 'man', value: 9 }),
    new Tile({ suit: 'pin', value: 1 })
  ];
  assert.ok(!isWinningHand(hand));
});
