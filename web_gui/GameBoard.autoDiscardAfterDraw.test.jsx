import { render } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';

function mockPlayers() {
  return new Array(4).fill(0).map(() => ({ hand: { tiles: Array(13), melds: [] }, river: [] }));
}

describe('GameBoard auto discard flow', () => {
  it('auto discards after auto draw on same turn', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true }));
    global.fetch = fetchMock;
    const players = mockPlayers();
    const state = {
      current_player: 1,
      players,
      wall: { tiles: [] },
      waiting_for_claims: [],
      last_discard: { suit: 'man', value: 1 },
    };
    const { rerender } = render(
      <GameBoard state={state} server="http://s" gameId="1" allowedActions={[[], ['draw'], [], []]} />,
    );
    await Promise.resolve();
    // after draw action
    players[1].hand.tiles.push({ suit: 'man', value: 1 });
    state.players = players;
    state.current_player = 1;
    rerender(
      <GameBoard state={state} server="http://s" gameId="1" allowedActions={[[], ['discard'], [], []]} />,
    );
    await Promise.resolve();
    const bodies = fetchMock.mock.calls
      .filter(c => c[1] && c[1].body)
      .map(c => JSON.parse(c[1].body));
    expect(bodies.at(-1)).toEqual({ player_index: 1, action: 'auto', ai_type: 'simple' });
  });
});
