import { test } from 'node:test';
import assert from 'node:assert';
import { Game } from '../src/index.js';

test('game dealing and turn flow', () => {
  const game = new Game(2); // two players for simplicity
  game.deal();
  for (const player of game.players) {
    assert.strictEqual(player.hand.length, 13);
  }
  const remaining = 136 - 13 * game.players.length;
  assert.strictEqual(game.wall.count, remaining);

  const tile = game.drawCurrent();
  assert.ok(tile);
  assert.strictEqual(game.players[0].hand.length, 14);
  const discarded = game.discardCurrent(game.players[0].hand.length - 1);
  assert.strictEqual(game.players[0].hand.length, 13);
  assert.strictEqual(game.players[0].discards[0], discarded);
  // current player should advance
  assert.strictEqual(game['currentIndex'], 1);
});
