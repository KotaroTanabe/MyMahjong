import { describe, it, expect } from 'vitest';
import { sortTiles } from './tileUtils.js';

describe('sortTiles', () => {
  it('sorts tiles by suit then value', () => {
    const tiles = [
      { suit: 'sou', value: 9 },
      { suit: 'man', value: 3 },
      { suit: 'pin', value: 1 },
      { suit: 'wind', value: 4 },
      { suit: 'dragon', value: 2 },
      { suit: 'man', value: 1 },
    ];
    const sorted = sortTiles(tiles);
    expect(sorted).toEqual([
      { suit: 'man', value: 1 },
      { suit: 'man', value: 3 },
      { suit: 'pin', value: 1 },
      { suit: 'sou', value: 9 },
      { suit: 'wind', value: 4 },
      { suit: 'dragon', value: 2 },
    ]);
  });
});
