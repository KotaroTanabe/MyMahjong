import { Tile } from './Tile.js';

export class Player {
  readonly hand: Tile[] = [];
  readonly discards: Tile[] = [];
  /**
   * Sets of tiles the player has called from other players.
   * Each meld is an array of tiles in the order they were claimed.
   */
  readonly melds: Tile[][] = [];

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

  canPon(tile: Tile): boolean {
    return this.hand.filter(t => t.toString() === tile.toString()).length >= 2;
  }

  pon(tile: Tile): void {
    if (!this.canPon(tile)) {
      throw new Error('Cannot pon: tile not found twice in hand');
    }
    const meld: Tile[] = [tile];
    let removed = 0;
    for (let i = this.hand.length - 1; i >= 0 && removed < 2; i--) {
      if (this.hand[i].toString() === tile.toString()) {
        meld.push(this.hand.splice(i, 1)[0]);
        removed++;
      }
    }
    if (removed !== 2) throw new Error('Unexpected tile count when pon');
    this.melds.push(meld);
  }
}
