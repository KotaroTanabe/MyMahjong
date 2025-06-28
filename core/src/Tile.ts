import type { TileType, Suit } from './types.js';

export class Tile {
  readonly suit: Suit;
  readonly value: string | number;

  constructor(type: TileType) {
    this.suit = type.suit;
    this.value = type.value;
  }

  toString(): string {
    return `${this.suit}-${this.value}`;
  }
}
