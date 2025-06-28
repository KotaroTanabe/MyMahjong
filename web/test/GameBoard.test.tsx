import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { GameBoard } from '../src/components/GameBoard.js';
import { Tile } from '@mymahjong/core';

test('GameBoard renders four player sections', () => {
  const tiles = [new Tile({ suit: 'man', value: 1 })];
  const html = renderToStaticMarkup(
    <GameBoard currentHand={tiles} onDiscard={() => {}} />
  );
  const count = (html.match(/class="player-area/g) || []).length;
  assert.equal(count, 4);
  assert.ok(html.includes('man-1'));
});
