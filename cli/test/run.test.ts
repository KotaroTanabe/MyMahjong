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
    calculateScore() {
      return {
        han: 0,
        fu: 20,
        rawFu: 20,
        basePoints: 0,
        rawPoints: 0,
        points: 0,
        yaku: [],
      };
    },
  } as any;

  const answers = ['', '0'];
  const rl: any = {
    question() { return Promise.resolve(answers.shift()); },
    close() {},
  };

  await run(game, rl);
  assert.strictEqual(game.wall.count, 0);
});

test('run prints discards', async () => {
  const game = {
    wall: { count: 1 },
    players: [{ hand: ['tile'], discards: [] }],
    deal() {},
    drawCurrent() { this.wall.count = 0; return 'drawn'; },
    discardCurrent() { this.players[0].discards.push('discarded'); return 'discarded'; },
    calculateScore() {
      return {
        han: 1,
        fu: 20,
        rawFu: 20,
        basePoints: 160,
        rawPoints: 640,
        points: 700,
        yaku: ['tanyao'],
      };
    },
  } as any;

  const answers = ['', '0'];
  const rl: any = {
    question() { return Promise.resolve(answers.shift()); },
    close() {},
  };

  const logs: string[] = [];
  const originalLog = console.log;
  console.log = (msg?: unknown) => { logs.push(String(msg)); };
  try {
    await run(game, rl);
  } finally {
    console.log = originalLog;
  }

  assert.ok(logs.includes('Your discards:'));
  assert.ok(logs.includes('discarded'));
});
