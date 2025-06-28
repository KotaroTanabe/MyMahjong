export function renderHand(hand: { toString(): string }[]): string {
  return hand.map((tile, i) => `[${i}] ${tile.toString()}`).join(' ');
}

export async function prompt(rl: import('node:readline/promises').Interface, question: string): Promise<string> {
  return rl.question(question);
}

