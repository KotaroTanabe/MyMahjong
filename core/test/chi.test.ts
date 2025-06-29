import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Game, Wall, Tile } from '../src/index.js';

test('player can call chi on a discard', () => {
  const wall = new Wall([]);
  const game = new Game(2, wall);
  game.players[1].hand.push(
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 3 })
  );
  const tile = new Tile({ suit: 'man', value: 2 });
  game.players[0].hand.push(tile);
  game.players[0].discard(0);
  game.callChi(1, 0);
  assert.strictEqual(game.players[1].melds.length, 1);
  assert.strictEqual(game.players[1].hand.length, 0);
  assert.deepStrictEqual(game.players[1].melds[0].map(t => t.value), [1,2,3]);
  assert.strictEqual(game['currentIndex'], 1);
});
