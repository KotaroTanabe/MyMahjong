import { render } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';

function mockPlayers() {
  return new Array(4).fill(0).map(() => ({ hand: { tiles: Array(13), melds: [] }, river: [] }));
}

describe('GameBoard consecutive auto discard', () => {
  it('auto discards for next player after auto draw', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true }));
    global.fetch = fetchMock;
    const players = mockPlayers();
    const state = {
      current_player: 2,
      players,
      wall: { tiles: [] },
      waiting_for_claims: [],
      last_discard: { suit: 'man', value: 1 },
    };
    const { rerender } = render(
      <GameBoard state={state} server="http://s" gameId="1" allowedActions={[[], [], ['draw'], []]} />,
    );
    await Promise.resolve();
    players[2].hand.tiles.push({ suit: 'man', value: 1 });
    state.players = players;
    rerender(
      <GameBoard state={state} server="http://s" gameId="1" allowedActions={[[], [], ['discard'], []]} />,
    );
    await Promise.resolve();
    const body = JSON.parse(fetchMock.mock.calls.at(-1)[1].body);
    expect(body).toEqual({ player_index: 2, action: 'auto', ai_type: 'simple' });
  });
});
