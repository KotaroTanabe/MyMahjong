import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { CenterDisplay } from '../src/components/CenterDisplay.js';
import { Tile } from '@mymahjong/core';

test('CenterDisplay shows dora indicators and wall count', () => {
  const tiles = [new Tile({ suit: 'man', value: 5 })];
  const html = renderToStaticMarkup(
    <CenterDisplay tiles={tiles} wallCount={70} />
  );
  assert.ok(html.includes('man-5.svg'));
  assert.ok(html.includes('70'));
});
