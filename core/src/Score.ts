import { Tile } from './Tile.js';
import type { Wind, Dragon } from './types.js';

export interface Meld {
  type: 'sequence' | 'triplet';
  tiles: Tile[];
}

export interface HandAnalysis {
  pair: Tile[];
  melds: Meld[];
}

export interface ScoreOptions {
  /** True if the winner is the dealer (oya) */
  dealer?: boolean;
  /** 'ron' for winning off a discard, 'tsumo' for self draw */
  win?: 'ron' | 'tsumo';
  /** Dora indicator tiles to count bonus han */
  doraIndicators?: Tile[];
  /** Adds one han if the player declared riichi */
  riichi?: boolean;
}

export interface ScoreResult {
  /** Names of all detected yaku */
  yaku: string[];
  /** Total han value */
  han: number;
  /** Fu after rounding up to the next 10 */
  fu: number;
  /** Fu before rounding */
  rawFu: number;
  /** Base points before any multipliers */
  basePoints: number;
  /** Final points after applying multipliers and rounding */
  points: number;
  /** Points before rounding to the nearest hundred */
  rawPoints: number;
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
 * Detects the "iipeikou" yaku (two identical sequences).
 * Sequences are identified using {@link analyzeHand} results.
 */
export function detectIipeikou(hand: Tile[]): boolean {
  if (detectSevenPairs(hand)) return false;
  const analysis = analyzeHand(hand);
  if (!analysis) return false;
  const sequences = analysis.melds
    .filter(m => m.type === 'sequence')
    .map(m => m.tiles.map(t => t.toString()).join(','));
  const counts = new Map<string, number>();
  for (const seq of sequences) {
    counts.set(seq, (counts.get(seq) ?? 0) + 1);
  }
  return [...counts.values()].some(c => c >= 2);
}

/**
 * Detects the "pinfu" yaku (all sequences with no extra fu). This simplified
 * version only checks that the hand is composed entirely of sequences, the pair
 * is not an honor tile and that fu calculation yields the base 20 fu. Wait
 * shapes are not analysed in detail.
 */
export function detectPinfu(hand: Tile[]): boolean {
  if (detectSevenPairs(hand)) return false;
  const analysis = analyzeHand(hand);
  if (!analysis) return false;
  if (!analysis.melds.every(m => m.type === 'sequence')) return false;
  const pairTile = analysis.pair[0];
  if (pairTile.suit === 'wind' || pairTile.suit === 'dragon') return false;
  return calculateFu(hand) === 20;
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

function doraFromIndicator(tile: Tile): string {
  if (tile.suit === 'man' || tile.suit === 'pin' || tile.suit === 'sou') {
    const value = tile.value as number;
    const next = value === 9 ? 1 : (value + 1) as 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;
    return `${tile.suit}-${next}`;
  }
  if (tile.suit === 'wind') {
    const order: Wind[] = ['east', 'south', 'west', 'north'];
    const idx = order.indexOf(tile.value as Wind);
    return `wind-${order[(idx + 1) % order.length]}`;
  }
  const dragons: Dragon[] = ['white', 'green', 'red'];
  const idx = dragons.indexOf(tile.value as Dragon);
  return `dragon-${dragons[(idx + 1) % dragons.length]}`;
}

function countDora(hand: Tile[], indicators: Tile[]): number {
  if (indicators.length === 0) return 0;
  const doraKeys = indicators.map(doraFromIndicator);
  return hand.filter(t => doraKeys.includes(t.toString())).length;
}

export function calculateScore(hand: Tile[], options: ScoreOptions = {}): ScoreResult {
  const { dealer = false, win = 'ron', doraIndicators = [], riichi = false } = options;
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
  if (detectIipeikou(hand)) {
    yaku.push('iipeikou');
    han += 1;
  }
  if (detectPinfu(hand)) {
    yaku.push('pinfu');
    han += 1;
  }
  if (doraIndicators.length > 0) {
    const doraCount = countDora(hand, doraIndicators);
    for (let i = 0; i < doraCount; i++) {
      yaku.push('dora');
    }
    han += doraCount;
  }
  if (riichi) {
    yaku.push('riichi');
    han += 1;
  }
  const rawFu = calculateFu(hand);
  const fu = Math.ceil(rawFu / 10) * 10;
  const basePoints = fu * 2 ** (han + 2);

  let rawPoints: number;
  let points: number;
  if (win === 'ron') {
    rawPoints = basePoints * (dealer ? 6 : 4);
    points = Math.ceil(rawPoints / 100) * 100;
  } else {
    if (dealer) {
      const share = Math.ceil((basePoints * 2) / 100) * 100;
      rawPoints = basePoints * 6;
      points = share * 3;
    } else {
      const fromDealer = Math.ceil((basePoints * 2) / 100) * 100;
      const fromNonDealer = Math.ceil(basePoints / 100) * 100;
      rawPoints = basePoints * 4;
      points = fromDealer + fromNonDealer * 2;
    }
  }

  return { yaku, han, fu, rawFu, basePoints, rawPoints, points };
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
