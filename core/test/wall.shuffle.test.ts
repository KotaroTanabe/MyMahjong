import { test } from 'node:test';
import assert from 'node:assert';
import { Wall, Tile } from '../src/index.js';

test('shuffle reorders tiles using supplied random', () => {
  const tiles = [1, 2, 3, 4].map(v => new Tile({ suit: 'man', value: v as 1|2|3|4 }));
  const wall = new Wall([...tiles]);
  wall.shuffle(() => 0); // deterministic shuffle
  const result = (wall as unknown as { tiles: Tile[] }).tiles;
  assert.deepStrictEqual(result.map(t => t.value), [2, 3, 4, 1]);
});
