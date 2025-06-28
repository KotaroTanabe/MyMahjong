import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';
import { Game } from '@mymahjong/core';
import { renderHand, prompt } from './UI.js';

export async function run(): Promise<void> {
  const rl = readline.createInterface({ input, output });
  const game = new Game(1);
  game.deal();
  const player = game.players[0];
  console.log('Your starting hand:');
  console.log(renderHand(player.hand));
  while (game.wall.count > 0) {
    await prompt(rl, 'Press Enter to draw');
    const drawn = game.drawCurrent();
    console.log(`You drew: ${drawn}`);
    console.log(renderHand(player.hand));
    const ans = await prompt(rl, 'Discard index: ');
    const index = parseInt(ans, 10);
    if (!Number.isFinite(index) || index < 0 || index >= player.hand.length) {
      console.log('Invalid index, try again.');
      continue;
    }
    const discarded = game.discardCurrent(index);
    console.log(`You discarded: ${discarded}`);
    console.log('Your hand:');
    console.log(renderHand(player.hand));
  }
  console.log('Wall exhausted, game over.');
  rl.close();
}

if (require.main === module) {
  run();
}

