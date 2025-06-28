import { test } from 'node:test';
import assert from 'node:assert';
import { prompt } from '../src/UI.js';

/* eslint-disable @typescript-eslint/no-explicit-any */

test('prompt forwards to readline', async () => {
  const asked: string[] = [];
  const rl: any = {
    question(q: string) {
      asked.push(q);
      return Promise.resolve('answer');
    },
  };
  const result = await prompt(rl, 'ask?');
  assert.strictEqual(result, 'answer');
  assert.deepStrictEqual(asked, ['ask?']);
});
