import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';
import { Game, ScoreResult } from '@mymahjong/core';
import { renderHand, renderDiscards, prompt } from './UI.js';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

export async function run(
  game: Game = new Game(1),
  rl: readline.Interface = readline.createInterface({ input, output })
): Promise<void> {
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
    const score: ScoreResult = game.calculateScore(0);
    if (score.han > 0) {
      console.log(`Possible yaku: ${score.yaku.join(', ')}`);
      console.log(`Han: ${score.han} Fu: ${score.fu} -> ${score.points} points`);
    }
    console.log('Your discards:');
    console.log(renderDiscards(player.discards));
  }
  console.log('Wall exhausted, game over.');
  rl.close();
}

const thisFile = fileURLToPath(import.meta.url);
dirname(thisFile);
if (process.argv[1] === thisFile) {
  run();
}

