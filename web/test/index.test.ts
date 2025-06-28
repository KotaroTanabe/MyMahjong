import { test } from 'node:test';
import assert from 'node:assert';
import { render } from '../src/index.js';

test('render returns 4', () => {
  assert.strictEqual(render(), 4);
});
