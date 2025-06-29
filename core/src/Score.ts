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

/**
 * Detects triplets of honor tiles (winds or dragons).
 * Returns an array of yakuhai names for each qualifying triplet.
 */
export function detectYakuhai(hand: Tile[]): string[] {
  const counts = new Map<string, { tile: Tile; count: number }>();
  for (const tile of hand) {
    const key = tile.toString();
    const entry = counts.get(key);
    if (entry) {
      entry.count += 1;
    } else {
      counts.set(key, { tile, count: 1 });
    }
  }

  const result: string[] = [];
  for (const { tile, count } of counts.values()) {
    if (count >= 3 && (tile.suit === 'wind' || tile.suit === 'dragon')) {
      result.push(`yakuhai-${tile.value}`);
    }
  }
  return result;
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
  const yakuhai = detectYakuhai(hand);
  if (yakuhai.length > 0) {
    yaku.push(...yakuhai);
    han += yakuhai.length;
  }
  const fu = 20;
  const points = han * fu;
  return { yaku, han, fu, points };
}

function canFormSets(counts: Map<string, number>, pairUsed: boolean): boolean {
  let first: string | undefined;
  for (const [tile, count] of counts) {
    if (count > 0) {
      first = tile;
      break;
    }
  }
  if (!first) return pairUsed;
  const [suit, valueStr] = first.split('-');
  const value = parseInt(valueStr, 10);

  // try pair
  if (!pairUsed && (counts.get(first) ?? 0) >= 2) {
    counts.set(first, (counts.get(first) ?? 0) - 2);
    if (canFormSets(counts, true)) return true;
    counts.set(first, (counts.get(first) ?? 0) + 2);
  }

  // try triplet
  if ((counts.get(first) ?? 0) >= 3) {
    counts.set(first, (counts.get(first) ?? 0) - 3);
    if (canFormSets(counts, pairUsed)) return true;
    counts.set(first, (counts.get(first) ?? 0) + 3);
  }

  // try sequence for number tiles
  if (suit === 'man' || suit === 'pin' || suit === 'sou') {
    const t1 = `${suit}-${value + 1}`;
    const t2 = `${suit}-${value + 2}`;
    if ((counts.get(first) ?? 0) > 0 && (counts.get(t1) ?? 0) > 0 && (counts.get(t2) ?? 0) > 0) {
      counts.set(first, (counts.get(first) ?? 0) - 1);
      counts.set(t1, (counts.get(t1) ?? 0) - 1);
      counts.set(t2, (counts.get(t2) ?? 0) - 1);
      if (canFormSets(counts, pairUsed)) return true;
      counts.set(first, (counts.get(first) ?? 0) + 1);
      counts.set(t1, (counts.get(t1) ?? 0) + 1);
      counts.set(t2, (counts.get(t2) ?? 0) + 1);
    }
  }
  return false;
}

export function isWinningHand(hand: Tile[]): boolean {
  if (detectSevenPairs(hand)) return true;
  if (hand.length !== 14) return false;
  const counts = new Map<string, number>();
  for (const tile of hand) {
    const key = tile.toString();
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return canFormSets(counts, false);
}
