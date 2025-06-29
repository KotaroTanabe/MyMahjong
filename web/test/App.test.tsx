import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import App from '../src/App.js';

test('App draw button has aria-label', () => {
  const html = renderToStaticMarkup(<App />);
  assert.ok(html.includes('aria-label="Draw"'));
});
