import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { Discards } from '../src/components/Discards.js';
import { Tile } from '@mymahjong/core';

test('Discards renders tiles', () => {
  const tiles = [new Tile({ suit: 'sou', value: 3 })];
  const html = renderToStaticMarkup(
    <Discards tiles={tiles} />
  );
  assert.ok(html.includes('<img'));
  assert.ok(html.includes('sou-3.svg'));
});
