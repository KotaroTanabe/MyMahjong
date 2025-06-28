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

export function detectSevenPairs(hand: Tile[]): boolean {
  if (hand.length !== 14) return false;
  const counts = new Map<string, number>();
  for (const tile of hand) {
    const key = tile.toString();
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return (
    counts.size === 7 &&
    [...counts.values()].every((count) => count === 2)
  );
}

export function calculateScore(hand: Tile[]): ScoreResult {
  const yaku: string[] = [];
  let han = 0;
  if (detectTanyao(hand)) {
    yaku.push('tanyao');
    han += 1;
  }
  if (detectSevenPairs(hand)) {
    yaku.push('chiitoitsu');
    han += 2;
  }
  const fu = 20;
  const points = han * fu;
  return { yaku, han, fu, points };
}
