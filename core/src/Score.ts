import { Tile } from './Tile.js';

export interface ScoreResult {
  yaku: string[];
  han: number;
  fu: number;
  points: number;
}

export function detectTanyao(hand: Tile[]): boolean {
  return hand.every(t => {
    if (t.suit === 'wind' || t.suit === 'dragon') return false;
    const v = t.value as number;
    return v >= 2 && v <= 8;
  });
}

export function calculateScore(hand: Tile[]): ScoreResult {
  const yaku: string[] = [];
  let han = 0;
  if (detectTanyao(hand)) {
    yaku.push('tanyao');
    han += 1;
  }
  const fu = 20;
  const points = han * fu;
  return { yaku, han, fu, points };
}
