import { render } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';

function startState() {
  return {
    current_player: 3,
    players: new Array(4).fill(0).map(() => ({ hand: { tiles: Array(13), melds: [] }, river: [] })),
    wall: { tiles: [] },
    waiting_for_claims: [1],
    last_discard: { suit: 'man', value: 1 },
  };
}

describe('GameBoard claim cleanup', () => {
  it('does not send extra auto after claims close', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true }));
    global.fetch = fetchMock;
    const state = startState();
    const { rerender } = render(
      <GameBoard
        state={state}
        server="http://s"
        gameId="1"
        allowedActions={[[], ['pon'], [], []]}
      />,
    );
    await Promise.resolve();
    fetchMock.mockClear();
    state.waiting_for_claims = [];
    state.current_player = 0;
    rerender(
      <GameBoard
        state={state}
        server="http://s"
        gameId="1"
        allowedActions={[['draw'], [], [], []]}
      />,
    );
    await Promise.resolve();
    const calls = fetchMock.mock.calls.filter(c => c[1] && c[1].body);
    expect(calls.length).toBe(0);
  });
});
