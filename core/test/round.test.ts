import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Game } from '../src/index.js';

const winds = ['east','south','west','north'] as const;

test('nextHand rotates dealer and round wind', () => {
  const game = new Game();
  assert.strictEqual(game.roundWind, 'east');
  game.nextHand();
  assert.strictEqual(game.roundWind, 'east');
  assert.deepStrictEqual(game.seatWinds, ['north','east','south','west']);
  game.nextHand();
  game.nextHand();
  game.nextHand();
  assert.strictEqual(game.roundWind, 'south');
  assert.deepStrictEqual(game.seatWinds, winds);
});
