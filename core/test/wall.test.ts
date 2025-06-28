import { test } from 'node:test';
import assert from 'node:assert';
import { Wall, Tile } from '../src/index.js';

function tileCounts(tiles: Tile[]): Map<string, number> {
  const map = new Map<string, number>();
  for (const t of tiles) {
    const key = t.toString();
    map.set(key, (map.get(key) || 0) + 1);
  }
  return map;
}

test('generateTiles creates 136 tiles with 4 of each kind', () => {
  const tiles = Wall.generateTiles();
  assert.strictEqual(tiles.length, 136);
  const counts = tileCounts(tiles);
  for (const count of counts.values()) {
    assert.strictEqual(count, 4);
  }
});

test('shuffled wall has same tiles but different order', () => {
  const wall = Wall.createShuffled(() => 0.5);
  const tiles = wall['tiles'] as unknown as Tile[]; // Access for test
  const unshuffled = Wall.generateTiles();
  assert.strictEqual(tiles.length, unshuffled.length);
  const sorted1 = [...tiles].map(t => t.toString()).sort().join(',');
  const sorted2 = unshuffled.map(t => t.toString()).sort().join(',');
  assert.strictEqual(sorted1, sorted2);
  // ensure order differs
  const serial1 = tiles.map(t => t.toString()).join(',');
  const serial2 = unshuffled.map(t => t.toString()).join(',');
  assert.notStrictEqual(serial1, serial2);
});
