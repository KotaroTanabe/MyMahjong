import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { Hand } from '../src/components/Hand.js';
import { Tile } from '@mymahjong/core';

test('Hand renders tile strings', () => {
  const tiles = [new Tile({ suit: 'man', value: 1 })];
  const html = renderToStaticMarkup(
    <Hand tiles={tiles} onDiscard={() => {}} />
  );
  assert.ok(html.includes('man-1'));
  assert.ok(html.includes('aria-label="Discard"'));
});
