import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { DiscardPile } from '../src/components/DiscardPile.js';
import { Tile } from '@mymahjong/core';

test('DiscardPile renders with orientation class', () => {
  const tiles = [new Tile({ suit: 'sou', value: 3 })];
  const html = renderToStaticMarkup(
    <DiscardPile tiles={tiles} position="left" />
  );
  assert.ok(html.includes('class="discard-pile left"'));
  assert.ok(html.includes('sou-3.svg'));
});
