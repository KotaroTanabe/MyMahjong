import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { ScoreBoard } from '../src/components/ScoreBoard.js';

const scores = [
  { wind: 'east' as const, points: 25000 },
  { wind: 'south' as const, points: 24000 },
];

test('ScoreBoard lists winds as icons and points', () => {
  const html = renderToStaticMarkup(<ScoreBoard scores={scores} />);
  assert.ok(html.includes('wind-east.svg'));
  assert.ok(html.includes('25000'));
  assert.ok(html.includes('wind-south.svg'));
  assert.ok(html.includes('24000'));
});
