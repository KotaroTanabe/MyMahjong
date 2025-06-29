import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { GameBoard } from '../src/components/GameBoard.js';
import { Tile } from '@mymahjong/core';

test('GameBoard renders hand, discards, melds and center tiles', () => {
  const tiles = [new Tile({ suit: 'man', value: 1 })];
  const discards = [new Tile({ suit: 'pin', value: 2 })];
  const discardsByPlayer = [discards, [], [], []];
  const melds = [[new Tile({ suit: 'sou', value: 3 })]];
  const center = [new Tile({ suit: 'wind', value: 'east' })];
  const html = renderToStaticMarkup(
    <GameBoard
      currentHand={tiles}
      playerDiscards={discardsByPlayer}
      currentMelds={melds}
      centerTiles={center}
      onDiscard={() => {}}
    />
  );
  const count = (html.match(/class="player-area/g) || []).length;
  assert.equal(count, 4);
  assert.ok(html.includes('man-1.svg'));
  assert.ok(html.includes('pin-2.svg'));
  assert.ok(html.includes('sou-3.svg'));
  assert.ok(html.includes('wind-east.svg'));
});
