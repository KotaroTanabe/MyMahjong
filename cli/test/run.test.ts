import { test } from 'node:test';
import assert from 'node:assert';
import { run } from '../src/index.js';

/* eslint-disable @typescript-eslint/no-explicit-any */

test('run processes a single turn', async () => {
  const game = {
    wall: { count: 1 },
    players: [{ hand: ['tile'], discards: [] }],
    deal() {},
    drawCurrent() { this.wall.count = 0; return 'drawn'; },
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    discardCurrent(index: number) { return 'discarded'; },
  } as any;

  const answers = ['', '0'];
  const rl: any = {
    question() { return Promise.resolve(answers.shift()); },
    close() {},
  };

  await run(game, rl);
  assert.strictEqual(game.wall.count, 0);
});
