# @mymahjong/core

The core package implements a very small subset of Mahjong mechanics in TypeScript. It defines the tiles, wall, player hands and a simple `Game` class for drawing and discarding tiles.

This package is framework agnostic and can be used from Node.js or the browser. See the tests in `test/` for basic usage examples.
The `Game` class also tracks the prevailing round wind. Calling `nextHand()` rotates the dealer and advances the round wind after each full rotation.

### Scoring Features

Currently implemented yaku detection includes:

- Tanyao (all simples)
- Chiitoitsu (seven pairs)
- Yakuhai (triplets of dragons or winds)
- Toitoi (all triplets)
- Iipeikou (two identical sequences)
- Ittsu (straight 1-9 in one suit)
- Pinfu (all sequences with no extra fu)
- Dora (bonus tiles from indicators)
- Riichi (declaring ready hand)
- Kan draws a replacement tile and reveals an extra dora indicator

Fu is calculated using a simplified model based on meld composition and honor
tiles. See `Score.ts` for details.
