import { test } from 'node:test';
import assert from 'node:assert';
import { Player, Wall } from '../src/index.js';

test('player draw and discard', () => {
  const wall = Wall.createShuffled(() => 0.5);
  const player = new Player();
  const tile = wall.draw();
  assert.ok(tile);
  player.draw(tile!);
  assert.strictEqual(player.hand.length, 1);
  const discarded = player.discard(0);
  assert.strictEqual(discarded, tile);
  assert.strictEqual(player.hand.length, 0);
  assert.strictEqual(player.discards.length, 1);
});

test('discard throws on invalid index', () => {
  const player = new Player();
  assert.throws(() => player.discard(0), /index out of range/i);
});
