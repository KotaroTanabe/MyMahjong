import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { Hand } from '../src/components/Hand.js';
import { Tile } from '@mymahjong/core';

test('Hand renders tile images', () => {
  const tiles = [new Tile({ suit: 'man', value: 1 })];
  const html = renderToStaticMarkup(
    <Hand tiles={tiles} onDiscard={() => {}} />
  );
  assert.ok(html.includes('<img'));
  assert.ok(html.includes('man-1.svg'));
  assert.ok(html.includes('aria-label="Discard"'));
  assert.ok(html.includes('class="tile-button"'));
});
