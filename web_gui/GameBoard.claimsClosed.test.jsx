import { render } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';

function mockState(waiting = [], player = 1) {
  return {
    current_player: player,
    players: new Array(4).fill(0).map(() => ({ hand: { tiles: Array(13), melds: [] }, river: [] })),
    wall: { tiles: [] },
    waiting_for_claims: waiting,
    last_discard: { suit: 'man', value: 1 },
  };
}

describe('GameBoard claims handling', () => {
  it('waits for claims to close before sending draw', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true }));
    global.fetch = fetchMock;
  const state = mockState([1], 1);
  const { rerender } = render(
    <GameBoard
      state={state}
      server="http://s"
      gameId="1"
      allowedActions={[["skip"], [], [], []]}
    />,
  );
  await Promise.resolve();
  fetchMock.mockClear();
  state.waiting_for_claims = [];
  rerender(
    <GameBoard
      state={state}
      server="http://s"
      gameId="1"
      allowedActions={[[], ["draw"], [], []]}
    />,
  );
  await Promise.resolve();
  const calls = fetchMock.mock.calls.filter(c => c[1] && c[1].body);
  const actions = calls.map(c => JSON.parse(c[1].body).action);
  expect(actions).not.toContain('draw');
  });
});
