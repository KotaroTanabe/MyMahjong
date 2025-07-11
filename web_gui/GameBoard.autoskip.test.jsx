import { render } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';

function mockState() {
  return {
    current_player: 1,
    players: new Array(4).fill(0).map(() => ({ hand: { tiles: Array(13), melds: [] }, river: [] })),
    wall: { tiles: [] },
    waiting_for_claims: [0],
    last_discard: { suit: 'man', value: 1 },
  };
}

describe('GameBoard auto skip', () => {
  it('sends skip when only skip allowed', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true }));
    global.fetch = fetchMock;
    const state = mockState();
    render(
      <GameBoard
        state={state}
        server="http://s"
        gameId="1"
        allowedActions={[['skip'], [], [], []]}
        claimOptions={[{ actions: ['skip'], chi: [] }, {}, {}, {}]}
      />,
    );
    await Promise.resolve();
    const bodies = fetchMock.mock.calls
      .filter(c => c[1] && c[1].body)
      .map(c => JSON.parse(c[1].body));
    expect(bodies).toContainEqual({ player_index: 0, action: 'skip' });
  });
});
