import { test } from 'node:test';
import assert from 'node:assert/strict';
import React, { forwardRef, useImperativeHandle } from 'react';
import { create, act } from 'react-test-renderer';
import { useGame } from '../src/hooks/useGame.js';
import { Game, Wall, Tile } from '@mymahjong/core';

interface GameHandle {
  hand: ReturnType<typeof useGame>['hand'];
  discards: ReturnType<typeof useGame>['discards'];
  score: ReturnType<typeof useGame>['score'];
  draw: () => unknown;
  discard: (index: number) => unknown;
}

function createFixedGame(): Game {
  const tiles = Array.from({ length: 20 }, () => new Tile({ suit: 'man', value: 2 }));
  const wall = new Wall(tiles);
  const g = new Game(1, wall);
  g.deal();
  return g;
}

const GameHarness = forwardRef<GameHandle>((_props, ref) => {
  const state = useGame(createFixedGame());
  useImperativeHandle(ref, () => state);
  return null;
});

GameHarness.displayName = 'GameHarness';

test('draw and discard update state', () => {
  const ref = React.createRef<GameHandle>();
  const renderer = create(<GameHarness ref={ref} />);
  assert.ok(ref.current);
  const initialHand = ref.current!.hand.length;
  const initialDiscards = ref.current!.discards.length;
  const initialPoints = ref.current!.score.points;

  act(() => {
    ref.current!.draw();
  });
  // after draw, hand should increase
  assert.strictEqual(ref.current!.hand.length, initialHand + 1);
  assert.ok(ref.current!.score.points >= initialPoints);

  act(() => {
    ref.current!.discard(ref.current!.hand.length - 1);
  });
  assert.strictEqual(ref.current!.hand.length, initialHand);
  assert.strictEqual(ref.current!.discards.length, initialDiscards + 1);

  renderer.unmount();
});
