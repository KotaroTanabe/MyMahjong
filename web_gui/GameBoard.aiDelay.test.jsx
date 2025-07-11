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

describe('GameBoard aiDelay', () => {
  it.skip('delays AI requests', async () => {
    vi.useFakeTimers();
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }));
    global.fetch = fetchMock;
    const state = mockState(1);
    render(
      <GameBoard
        state={state}
        server="http://s"
        gameId="1"
        aiDelay={500}
        allowedActions={[['draw'], [], [], []]}
        claimOptions={[{ actions: [], chi: [] }, {}, {}, {}]}
      />,
    );
    await vi.runAllTicks();
    const before = fetchMock.mock.calls.filter(c => c[0].includes('/action'));
    expect(before.length).toBe(0);
    await vi.advanceTimersByTimeAsync(500);
    const after = fetchMock.mock.calls.filter(c => c[0].includes('/action'));
    expect(after.length).toBe(1);
    vi.useRealTimers();
  });
});
