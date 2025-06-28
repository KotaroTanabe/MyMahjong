import { test } from 'node:test';
import assert from 'node:assert';
import { Tile } from '@mymahjong/core';
import { renderHand, renderDiscards } from '../src/UI.js';

/* eslint-disable @typescript-eslint/no-explicit-any */

function makeTile(label: string): Tile {
  const [suit, value] = label.split('-');
  return new Tile({ suit: suit as any, value: isNaN(Number(value)) ? value as any : Number(value) as any });
}

test('renderHand lists tiles with indexes', () => {
  const hand = ['man-1', 'pin-2', 'sou-3'].map(makeTile);
  const result = renderHand(hand);
  assert.strictEqual(result, '[0] man-1 [1] pin-2 [2] sou-3');
});

test('renderDiscards joins tiles', () => {
  const discards = ['man-1', 'sou-9'].map(makeTile);
  const result = renderDiscards(discards);
  assert.strictEqual(result, 'man-1 sou-9');
});

test('renderDiscards handles empty list', () => {
  const result = renderDiscards([]);
  assert.strictEqual(result, '(none)');
});

