import { test } from 'node:test';
import assert from 'node:assert';
import { sum } from '../src/index.js';

test('sum adds numbers', () => {
  assert.strictEqual(sum(1, 2), 3);
});
