import { render } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';

function mockState(playerIndex = 1) {
  return {
    current_player: playerIndex,
    players: new Array(4).fill(0).map(() => ({ hand: { tiles: Array(13), melds: [] }, river: [] })),
    wall: { tiles: [] },
    waiting_for_claims: [],
    last_discard: { suit: 'man', value: 1 },
  };
}

describe('GameBoard auto guard', () => {
  it('skips auto when no longer allowed', async () => {
    vi.useFakeTimers();
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true }));
    global.fetch = fetchMock;
    const state = mockState(1);
    const { rerender } = render(
      <GameBoard state={state} server="http://s" gameId="1" aiDelay={500} allowedActions={[['draw'], [], [], []]} />,
    );
    await vi.runAllTicks();
    rerender(
      <GameBoard state={state} server="http://s" gameId="1" aiDelay={500} allowedActions={[[], [], [], []]} />,
    );
    await vi.advanceTimersByTimeAsync(500);
    const calls = fetchMock.mock.calls.filter(c => c[0].includes('/action'));
    expect(calls.length).toBe(0);
    vi.useRealTimers();
  });
});
