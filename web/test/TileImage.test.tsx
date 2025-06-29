import { test } from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import { create, act } from 'react-test-renderer';
import { TileImage } from '../src/components/TileImage.js';
import { Tile } from '@mymahjong/core';

test('TileImage falls back to emoji when image fails', () => {
  const tile = new Tile({ suit: 'man', value: 1 });
  const renderer = create(<TileImage tile={tile} />);
  const img = renderer.root.findByType('img');
  act(() => {
    img.props.onError();
  });
  const span = renderer.root.findByType('span');
  assert.equal(span.props.role, 'img');
  assert.equal(span.props['aria-label'], 'man 1');
  assert.equal(span.children[0], '🀄');
  renderer.unmount();
});
