import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { Melds } from '../src/components/Melds.js';
import { Tile } from '@mymahjong/core';

test('Melds renders sets of tiles', () => {
  const melds = [[
    new Tile({ suit: 'man', value: 1 }),
    new Tile({ suit: 'man', value: 2 }),
    new Tile({ suit: 'man', value: 3 }),
  ]];
  const html = renderToStaticMarkup(<Melds melds={melds} />);
  assert.ok(html.includes('man-1'));
  assert.ok(html.includes('man-2'));
  assert.ok(html.includes('man-3'));
});
