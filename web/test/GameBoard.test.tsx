import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { GameBoard } from '../src/components/GameBoard.js';
import { Tile } from '@mymahjong/core';

test('GameBoard renders hand, discards and melds', () => {
  const tiles = [new Tile({ suit: 'man', value: 1 })];
  const discards = [new Tile({ suit: 'pin', value: 2 })];
  const melds = [[new Tile({ suit: 'sou', value: 3 })]];
  const html = renderToStaticMarkup(
    <GameBoard
      currentHand={tiles}
      currentDiscards={discards}
      currentMelds={melds}
      onDiscard={() => {}}
    />
  );
  const count = (html.match(/class="player-area/g) || []).length;
  assert.equal(count, 4);
  assert.ok(html.includes('man-1.svg'));
  assert.ok(html.includes('pin-2.svg'));
  assert.ok(html.includes('sou-3.svg'));
  assert.ok(html.includes('class="discard-pile bottom"'));
  assert.ok(html.includes('class="discard-pile top"'));
  assert.ok(html.includes('class="discard-pile left"'));
  assert.ok(html.includes('class="discard-pile right"'));
});
