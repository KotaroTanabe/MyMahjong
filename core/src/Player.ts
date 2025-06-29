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

  canChi(tile: Tile): boolean {
    if (tile.suit === 'wind' || tile.suit === 'dragon') return false;
    const counts = new Map<number, number>();
    for (const t of this.hand) {
      if (t.suit === tile.suit) {
        const v = t.value as number;
        counts.set(v, (counts.get(v) ?? 0) + 1);
      }
    }
    const v = tile.value as number;
    const sequences: [number, number][] = [
      [v - 2, v - 1],
      [v - 1, v + 1],
      [v + 1, v + 2],
    ];
    for (const [a, b] of sequences) {
      if (a >= 1 && b <= 9 && (counts.get(a) ?? 0) > 0 && (counts.get(b) ?? 0) > 0) {
        return true;
      }
    }
    return false;
  }

  chi(tile: Tile): void {
    if (!this.canChi(tile)) {
      throw new Error('Cannot chi: tiles not found in hand');
    }
    const suit = tile.suit;
    const v = tile.value as number;
    const sequences: [number, number][] = [
      [v - 2, v - 1],
      [v - 1, v + 1],
      [v + 1, v + 2],
    ];
    for (const [a, b] of sequences) {
      if (a < 1 || b > 9) continue;
      const indexA = this.hand.findIndex(t => t.suit === suit && t.value === a);
      if (indexA === -1) continue;
      const indexB = this.hand.findIndex((t, idx) => t.suit === suit && t.value === b && idx !== indexA);
      if (indexB === -1) continue;
      const first = Math.max(indexA, indexB);
      const second = Math.min(indexA, indexB);
      const tileA = this.hand.splice(first, 1)[0];
      const tileB = this.hand.splice(second, 1)[0];
      const meld = [tileA, tile, tileB].sort((x, y) => (x.value as number) - (y.value as number));
      this.melds.push(meld);
      return;
    }
    throw new Error('Cannot chi: sequence not found');
  }

  canKan(tile: Tile): boolean {
    return this.hand.filter(t => t.toString() === tile.toString()).length >= 3;
  }

  kan(tile: Tile): void {
    if (!this.canKan(tile)) {
      throw new Error('Cannot kan: tile not found three times in hand');
    }
    const meld: Tile[] = [tile];
    let removed = 0;
    for (let i = this.hand.length - 1; i >= 0 && removed < 3; i--) {
      if (this.hand[i].toString() === tile.toString()) {
        meld.push(this.hand.splice(i, 1)[0]);
        removed++;
      }
    }
    if (removed !== 3) throw new Error('Unexpected tile count when kan');
    this.melds.push(meld);
  }
}
