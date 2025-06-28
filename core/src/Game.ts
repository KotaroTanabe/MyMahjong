import { Player } from './Player.js';
import { Wall } from './Wall.js';
import { Tile } from './Tile.js';
import { calculateScore, ScoreResult } from './Score.js';

export class Game {
  readonly wall: Wall;
  readonly players: Player[];
  private currentIndex = 0;

  constructor(playerCount = 4, wall: Wall = Wall.createShuffled()) {
    this.wall = wall;
    this.players = Array.from({ length: playerCount }, () => new Player());
  }

  deal(initialHandSize = 13): void {
    for (let i = 0; i < initialHandSize; i++) {
      for (const player of this.players) {
        const tile = this.wall.draw();
        if (!tile) throw new Error('Wall exhausted');
        player.draw(tile);
      }
    }
  }

  drawCurrent(): Tile {
    const tile = this.wall.draw();
    if (!tile) throw new Error('Wall exhausted');
    this.players[this.currentIndex].draw(tile);
    return tile;
  }

  discardCurrent(index: number): Tile {
    const tile = this.players[this.currentIndex].discard(index);
    this.currentIndex = (this.currentIndex + 1) % this.players.length;
    return tile;
  }

  calculateScore(playerIndex = this.currentIndex): ScoreResult {
    return calculateScore(this.players[playerIndex].hand);
  }
}
