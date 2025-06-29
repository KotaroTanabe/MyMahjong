import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Game } from '../src/index.js';

const winds = ['east','south','west','north'] as const;

test('game assigns seat winds to players', () => {
  const game = new Game();
  for (let i = 0; i < game.players.length; i++) {
    assert.strictEqual(game.players[i].seatWind, winds[i]);
  }
});

test('rotateDealer advances dealer and seat winds', () => {
  const game = new Game();
  game.rotateDealer();
  const expected = ['north','east','south','west'] as const;
  for (let i = 0; i < game.players.length; i++) {
    assert.strictEqual(game.players[i].seatWind, expected[i]);
  }
  assert.strictEqual(game['dealerIndex'], 1);
});
