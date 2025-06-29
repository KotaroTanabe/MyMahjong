import { test } from 'node:test';
import assert from 'node:assert/strict';
import React, { forwardRef, useImperativeHandle } from 'react';
import { create, act } from 'react-test-renderer';
import { useGame } from '../src/hooks/useGame.js';
import { Game, Wall, Tile } from '@mymahjong/core';

interface GameHandle {
  hand: ReturnType<typeof useGame>['hand'];
  discards: ReturnType<typeof useGame>['discards'];
  playerDiscards: ReturnType<typeof useGame>['playerDiscards'];
  score: ReturnType<typeof useGame>['score'];
  draw: () => unknown;
  discard: (index: number) => unknown;
  pon: (fromIndex: number) => unknown;
  chi: (fromIndex: number) => unknown;
}

function createFixedGame(): Game {
  const tiles = Array.from({ length: 20 }, () => new Tile({ suit: 'man', value: 2 }));
  const wall = new Wall(tiles);
  const g = new Game(1, wall);
  g.deal();
  return g;
}

function createPonGame(): Game {
  const wall = new Wall([]);
  const g = new Game(2, wall);
  g.players[0].hand.push(new Tile({ suit: 'man', value: 3 }), new Tile({ suit: 'man', value: 3 }));
  const discarded = new Tile({ suit: 'man', value: 3 });
  g.players[1].hand.push(discarded);
  g.players[1].discard(0);
  return g;
}

function createChiGame(): Game {
  const wall = new Wall([]);
  const g = new Game(2, wall);
  g.players[0].hand.push(new Tile({ suit: 'man', value: 1 }), new Tile({ suit: 'man', value: 3 }));
  const discarded = new Tile({ suit: 'man', value: 2 });
  g.players[1].hand.push(discarded);
  g.players[1].discard(0);
  return g;
}

const GameHarness = forwardRef<GameHandle>((_props, ref) => {
  const state = useGame(createFixedGame());
  useImperativeHandle(ref, () => state);
  return null;
});

GameHarness.displayName = 'GameHarness';

const PonHarness = forwardRef<GameHandle>((_props, ref) => {
  const state = useGame(createPonGame());
  useImperativeHandle(ref, () => state);
  return null;
});

PonHarness.displayName = 'PonHarness';

const ChiHarness = forwardRef<GameHandle>((_props, ref) => {
  const state = useGame(createChiGame());
  useImperativeHandle(ref, () => state);
  return null;
});

ChiHarness.displayName = 'ChiHarness';

test('draw and discard update state', () => {
  const ref = React.createRef<GameHandle>();
  const renderer = create(<GameHarness ref={ref} />);
  assert.ok(ref.current);
  const initialHand = ref.current!.hand.length;
  const initialDiscards = ref.current!.discards.length;
  const initialPlayerDiscards = ref.current!.playerDiscards.map(d => d.length);
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
  assert.strictEqual(
    ref.current!.playerDiscards[0].length,
    initialPlayerDiscards[0] + 1
  );

  renderer.unmount();
});

test('pon updates melds and discards', () => {
  const ref = React.createRef<GameHandle>();
  const renderer = create(<PonHarness ref={ref} />);
  assert.ok(ref.current);
  const initialHand = ref.current!.hand.length;
  const initialOpponentDiscards = ref.current!.playerDiscards[1].length;

  act(() => {
    ref.current!.pon(1);
  });

  assert.strictEqual(ref.current!.playerDiscards[1].length, initialOpponentDiscards - 1);
  assert.strictEqual(ref.current!.hand.length, initialHand - 2);

  renderer.unmount();
});

test('chi updates melds and discards', () => {
  const ref = React.createRef<GameHandle>();
  const renderer = create(<ChiHarness ref={ref} />);
  assert.ok(ref.current);
  const initialHand = ref.current!.hand.length;
  const initialOpponentDiscards = ref.current!.playerDiscards[1].length;

  act(() => {
    ref.current!.chi(1);
  });

  assert.strictEqual(ref.current!.playerDiscards[1].length, initialOpponentDiscards - 1);
  assert.strictEqual(ref.current!.hand.length, initialHand - 2);

  renderer.unmount();
});
