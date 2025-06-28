import { Tile } from './Tile.js';

export class Player {
  readonly hand: Tile[] = [];
  readonly discards: Tile[] = [];

  draw(tile: Tile): void {
    this.hand.push(tile);
  }

  discard(index: number): Tile {
    if (index < 0 || index >= this.hand.length) {
      throw new Error('Index out of range');
    }
    const [tile] = this.hand.splice(index, 1);
    this.discards.push(tile);
    return tile;
  }
}
