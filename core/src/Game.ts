import { Player } from './Player.js';
import { Wall } from './Wall.js';
import { Tile } from './Tile.js';
import { calculateScore, ScoreResult, isWinningHand } from './Score.js';

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

  callPon(playerIndex: number, fromIndex: number): void {
    const from = this.players[fromIndex];
    const tile = from.discards.pop();
    if (!tile) throw new Error('No discard to claim');
    const player = this.players[playerIndex];
    if (!player.canPon(tile)) {
      from.discards.push(tile);
      throw new Error('Player cannot pon this tile');
    }
    player.pon(tile);
    this.currentIndex = playerIndex;
  }

  declareRon(playerIndex: number, fromIndex: number): boolean {
    const tile = this.players[fromIndex].discards.at(-1);
    if (!tile) throw new Error('No discard to claim');
    const hand = [...this.players[playerIndex].hand, tile];
    return isWinningHand(hand);
  }

  calculateScore(playerIndex = this.currentIndex): ScoreResult {
    return calculateScore(this.players[playerIndex].hand);
  }

  isWinningHand(playerIndex = this.currentIndex): boolean {
    return isWinningHand(this.players[playerIndex].hand);
  }
}
