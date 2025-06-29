import { Tile } from './Tile.js';
import type { Dragon, NumberSuit, Wind } from './types.js';

export class Wall {
  private tiles: Tile[];

  constructor(tiles: Tile[] = []) {
    this.tiles = tiles;
  }

  static generateTiles(): Tile[] {
    const tiles: Tile[] = [];
    const numberSuits: NumberSuit[] = ['man', 'pin', 'sou'];
    for (const suit of numberSuits) {
      for (let value = 1 as const; value <= 9; value++) {
        for (let i = 0; i < 4; i++) {
          tiles.push(new Tile({ suit, value: value as 1|2|3|4|5|6|7|8|9 }));
        }
      }
    }

    const winds: Wind[] = ['east', 'south', 'west', 'north'];
    for (const value of winds) {
      for (let i = 0; i < 4; i++) {
        tiles.push(new Tile({ suit: 'wind', value }));
      }
    }

    const dragons: Dragon[] = ['white', 'green', 'red'];
    for (const value of dragons) {
      for (let i = 0; i < 4; i++) {
        tiles.push(new Tile({ suit: 'dragon', value }));
      }
    }
    return tiles;
  }

  static createShuffled(random: () => number = Math.random): Wall {
    const tiles = Wall.generateTiles();
    // Fisher-Yates shuffle
    for (let i = tiles.length - 1; i > 0; i--) {
      const j = Math.floor(random() * (i + 1));
      [tiles[i], tiles[j]] = [tiles[j], tiles[i]];
    }
    return new Wall(tiles);
  }

  shuffle(random: () => number = Math.random): void {
    for (let i = this.tiles.length - 1; i > 0; i--) {
      const j = Math.floor(random() * (i + 1));
      [this.tiles[i], this.tiles[j]] = [this.tiles[j], this.tiles[i]];
    }
  }

  draw(): Tile | undefined {
    return this.tiles.pop();
  }

  /** Peek at a tile without removing it. 0 refers to the next tile to be drawn. */
  peek(index = 0): Tile | undefined {
    return this.tiles[this.tiles.length - 1 - index];
  }

  get count(): number {
    return this.tiles.length;
  }
}
