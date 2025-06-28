import { test } from 'node:test';
import assert from 'node:assert/strict';
import React, { forwardRef, useImperativeHandle } from 'react';
import { create, act } from 'react-test-renderer';
import { useGame } from '../src/hooks/useGame.js';

interface GameHandle {
  hand: ReturnType<typeof useGame>['hand'];
  discards: ReturnType<typeof useGame>['discards'];
  draw: () => unknown;
  discard: (index: number) => unknown;
}

const GameHarness = forwardRef<GameHandle>((_props, ref) => {
  const state = useGame();
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

  act(() => {
    ref.current!.draw();
  });
  // after draw, hand should increase
  assert.strictEqual(ref.current!.hand.length, initialHand + 1);

  act(() => {
    ref.current!.discard(ref.current!.hand.length - 1);
  });
  assert.strictEqual(ref.current!.hand.length, initialHand);
  assert.strictEqual(ref.current!.discards.length, initialDiscards + 1);

  renderer.unmount();
});
