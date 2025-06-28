import { test } from 'node:test';
import assert from 'node:assert';
import { run } from '../src/index.js';

test('run returns 3', () => {
  assert.strictEqual(run(), 3);
});
