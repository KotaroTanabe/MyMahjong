import { Tile } from './Tile.js';

export interface Meld {
  type: 'sequence' | 'triplet';
  tiles: Tile[];
}

export interface HandAnalysis {
  pair: Tile[];
  melds: Meld[];
}

export interface ScoreResult {
  yaku: string[];
  han: number;
  fu: number;
  points: number;
}

/**
 * Returns true if the hand consists entirely of triplets (or quads) and a pair.
 * The function assumes a complete 14 tile hand.
 */
export function detectToitoi(hand: Tile[]): boolean {
  const analysis = analyzeHand(hand);
  return analysis !== null && analysis.melds.every(m => m.type === 'triplet');
}

/**
 * Very small fu calculation used for score examples.
 * - Base fu: 20
 * - +2 fu if the pair is an honor tile
 * - +2 fu for each triplet of simples, +4 fu for each triplet of honors
 */
export function calculateFu(hand: Tile[]): number {
  const analysis = analyzeHand(hand);
  if (!analysis) return 0;
  let fu = 20;
  const pairTile = analysis.pair[0];
  if (pairTile.suit === 'wind' || pairTile.suit === 'dragon') {
    fu += 2;
  }
  for (const meld of analysis.melds) {
    if (meld.type === 'triplet') {
      const tile = meld.tiles[0];
      const isHonor = tile.suit === 'wind' || tile.suit === 'dragon';
      fu += isHonor ? 4 : 2;
    }
  }
  return fu;
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
  if (detectToitoi(hand)) {
    yaku.push('toitoi');
    han += 2;
  }
  const fu = calculateFu(hand);
  const points = han * fu;
  return { yaku, han, fu, points };
}


export function isWinningHand(hand: Tile[]): boolean {
  if (detectSevenPairs(hand)) return true;
  return analyzeHand(hand) !== null;
}

export function analyzeHand(hand: Tile[]): HandAnalysis | null {
  if (hand.length !== 14) return null;
  const counts = new Map<string, number>();
  const samples = new Map<string, Tile>();
  for (const tile of hand) {
    const key = tile.toString();
    counts.set(key, (counts.get(key) ?? 0) + 1);
    if (!samples.has(key)) samples.set(key, tile);
  }
  return search(counts, null, [], samples);
}

function search(
  counts: Map<string, number>,
  pair: Tile[] | null,
  melds: Meld[],
  samples: Map<string, Tile>
): HandAnalysis | null {
  let first: string | undefined;
  for (const [tile, count] of counts) {
    if (count > 0) {
      first = tile;
      break;
    }
  }
  if (!first) {
    if (pair && melds.length === 4) {
      return { pair, melds: [...melds] };
    }
    return null;
  }

  const [suit, valueStr] = first.split('-');
  const value = parseInt(valueStr, 10);
  const tileObj = samples.get(first)!;

  if (!pair && (counts.get(first) ?? 0) >= 2) {
    counts.set(first, (counts.get(first) ?? 0) - 2);
    const result = search(counts, [tileObj, tileObj], melds, samples);
    if (result) return result;
    counts.set(first, (counts.get(first) ?? 0) + 2);
  }

  if ((counts.get(first) ?? 0) >= 3) {
    counts.set(first, (counts.get(first) ?? 0) - 3);
    melds.push({ type: 'triplet', tiles: [tileObj, tileObj, tileObj] });
    const result = search(counts, pair, melds, samples);
    if (result) return result;
    melds.pop();
    counts.set(first, (counts.get(first) ?? 0) + 3);
  }

  if (suit === 'man' || suit === 'pin' || suit === 'sou') {
    const t1 = `${suit}-${value + 1}`;
    const t2 = `${suit}-${value + 2}`;
    if (
      (counts.get(first) ?? 0) > 0 &&
      (counts.get(t1) ?? 0) > 0 &&
      (counts.get(t2) ?? 0) > 0
    ) {
      counts.set(first, (counts.get(first) ?? 0) - 1);
      counts.set(t1, (counts.get(t1) ?? 0) - 1);
      counts.set(t2, (counts.get(t2) ?? 0) - 1);
      const seq = [samples.get(first)!, samples.get(t1)!, samples.get(t2)!].sort(
        (a, b) => (a.value as number) - (b.value as number)
      );
      melds.push({ type: 'sequence', tiles: seq });
      const result = search(counts, pair, melds, samples);
      if (result) return result;
      melds.pop();
      counts.set(first, (counts.get(first) ?? 0) + 1);
      counts.set(t1, (counts.get(t1) ?? 0) + 1);
      counts.set(t2, (counts.get(t2) ?? 0) + 1);
    }
  }
  return null;
}
