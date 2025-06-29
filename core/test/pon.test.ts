import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Game, Wall, Tile } from '../src/index.js';

// Player 1 discards a tile, Player 2 calls pon on it

test('player can call pon on a discard', () => {
  const wall = new Wall([]);
  const game = new Game(2, wall);
  const tile = new Tile({ suit: 'man', value: 3 });
  game.players[0].hand.push(tile);
  game.players[1].hand.push(new Tile({ suit: 'man', value: 3 }));
  game.players[1].hand.push(new Tile({ suit: 'man', value: 3 }));

  game.players[0].discard(0);
  game.callPon(1, 0);

  assert.strictEqual(game.players[1].melds.length, 1);
  assert.strictEqual(game.players[1].hand.length, 0);
  assert.strictEqual(game.players[1].melds[0].length, 3);
  // turn should pass to player 2
  assert.strictEqual(game['currentIndex'], 1);
});
