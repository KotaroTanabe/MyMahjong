/**
 * Convert tiles to their string representation.
 * Keeping this logic in one place makes the UI easier to extend later
 * (e.g. adding colors or Unicode characters).
 */
export function tileStrings(tiles: { toString(): string }[]): string[] {
  return tiles.map((tile) => tile.toString());
}

export function renderHand(hand: { toString(): string }[]): string {
  return tileStrings(hand)
    .map((label, i) => `[${i}] ${label}`)
    .join(' ');
}

export function renderDiscards(discards: { toString(): string }[]): string {
  const labels = tileStrings(discards);
  if (labels.length === 0) return '(none)';
  return labels.join(' ');
}

export async function prompt(rl: import('node:readline/promises').Interface, question: string): Promise<string> {
  return rl.question(question);
}

