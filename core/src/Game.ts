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

  callChi(playerIndex: number, fromIndex: number): void {
    const from = this.players[fromIndex];
    const tile = from.discards.pop();
    if (!tile) throw new Error('No discard to claim');
    const player = this.players[playerIndex];
    if (!player.canChi(tile)) {
      from.discards.push(tile);
      throw new Error('Player cannot chi this tile');
    }
    player.chi(tile);
    this.currentIndex = playerIndex;
  }

  callKan(playerIndex: number, fromIndex: number): void {
    const from = this.players[fromIndex];
    const tile = from.discards.pop();
    if (!tile) throw new Error('No discard to claim');
    const player = this.players[playerIndex];
    if (!player.canKan(tile)) {
      from.discards.push(tile);
      throw new Error('Player cannot kan this tile');
    }
    player.kan(tile);
    this.currentIndex = playerIndex;
  }

  declareRon(playerIndex: number, fromIndex: number): boolean {
    const from = this.players[fromIndex];
    const tile = from.discards.at(-1);
    if (!tile) throw new Error('No discard to claim');
    const hand = [...this.players[playerIndex].hand, tile];
    if (isWinningHand(hand)) {
      from.discards.pop();
      this.players[playerIndex].hand.push(tile);
      this.currentIndex = playerIndex;
      return true;
    }
    return false;
  }

  calculateScore(
    playerIndex = this.currentIndex,
    options: import('./Score.js').ScoreOptions = {}
  ): ScoreResult {
    return calculateScore(this.players[playerIndex].hand, options);
  }

  isWinningHand(playerIndex = this.currentIndex): boolean {
    return isWinningHand(this.players[playerIndex].hand);
  }
}
