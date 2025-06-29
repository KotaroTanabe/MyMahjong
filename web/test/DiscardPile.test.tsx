import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { DiscardPile } from '../src/components/DiscardPile.js';
import { Tile } from '@mymahjong/core';

function createTiles(n: number): Tile[] {
  return Array.from({ length: n }, (_, i) => {
    const value = ((i % 9) + 1) as 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;
    return new Tile({ suit: 'man', value });
  });
}

test('DiscardPile groups tiles into rows of six', () => {
  const tiles = createTiles(8);
  const html = renderToStaticMarkup(<DiscardPile tiles={tiles} />);
  const rowCount = (html.match(/<ul>/g) || []).length;
  assert.strictEqual(rowCount, 2);
  const firstRow = html.split('</ul>')[0];
  const imgCount = (firstRow.match(/<img/g) || []).length;
  assert.strictEqual(imgCount, 6);
});

test('position prop adds orientation class', () => {
  const tiles = createTiles(1);
  const html = renderToStaticMarkup(<DiscardPile tiles={tiles} position="top" />);
  assert.ok(html.includes('class="discard-pile top"'));
});
