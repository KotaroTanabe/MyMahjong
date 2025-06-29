import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Game, Wall, Tile } from '../src/index.js';

function winningTiles(): Tile[] {
  // simple hand: 1-2-3 man, 4-5-6 man, 7-8-9 man, triplet of pin1, pair of pin2
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
  ];
}

test('declareRon detects win with discard', () => {
  const wall = new Wall([]);
  const game = new Game(2, wall);
  game.players[1].hand.push(...winningTiles());
  const winningTile = new Tile({ suit: 'pin', value: 2 });
  game.players[0].hand.push(winningTile);
  game.players[0].discard(0);
  assert.ok(game.declareRon(1, 0));
  assert.strictEqual(game.players[0].discards.length, 0);
  assert.strictEqual(game.players[1].hand.length, 14);
});
