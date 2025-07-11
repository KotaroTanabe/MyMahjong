import { render, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';

function mockState(playerIndex = 0, waiting = []) {
  return {
    current_player: playerIndex,
    players: new Array(4).fill(0).map(() => ({ hand: { tiles: Array(13), melds: [] }, river: [] })),
    wall: { tiles: [] },
    waiting_for_claims: waiting,
    last_discard: { suit: 'man', value: 1 },
  };
}

describe('GameBoard auto draw', () => {
  it('requests draw or auto when current_player changes', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }));
    global.fetch = fetchMock;
    const state = mockState(0);
    const { rerender, getAllByLabelText } = render(
      <GameBoard state={state} server="http://s" gameId="1" />,
    );
    await Promise.resolve();
    const drawCall = fetchMock.mock.calls.find(c => c[0].includes('/action'));
    expect(JSON.parse(drawCall[1].body)).toEqual({ player_index: 0, action: 'draw' });
    fetchMock.mockClear();
    state.current_player = 1;
    state.waiting_for_claims = [1, 2, 3];
    rerender(
      <GameBoard
        state={state}
        server="http://s"
        gameId="1"
        allowedActions={[[], ['chi'], ['chi'], ['chi']]}
      />,
    );
    await Promise.resolve();
    const bodies = fetchMock.mock.calls
      .filter(c => c[1] && c[1].body)
      .map(c => JSON.parse(c[1].body));
    expect(bodies).toContainEqual({ player_index: 1, action: 'auto', ai_type: 'simple' });
    expect(bodies).toContainEqual({ player_index: 2, action: 'auto', ai_type: 'simple' });
    expect(bodies).toContainEqual({ player_index: 3, action: 'auto', ai_type: 'simple' });
    fetchMock.mockClear();
    state.waiting_for_claims = [];
    fireEvent.click(getAllByLabelText('Enable AI')[0]);
    await Promise.resolve();
    state.current_player = 0;
    rerender(<GameBoard state={state} server="http://s" gameId="1" />);
    await Promise.resolve();
    const bodies2 = fetchMock.mock.calls
      .filter(c => c[1] && c[1].body)
      .map(c => JSON.parse(c[1].body));
    expect(bodies2).toContainEqual({ player_index: 0, action: 'auto', ai_type: 'simple' });
  });

  it('does not auto play when result is shown', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true }));
    global.fetch = fetchMock;
    const state = { ...mockState(0), result: { type: 'ryukyoku' } };
    const { rerender } = render(
      <GameBoard state={state} server="http://s" gameId="1" />,
    );
    await Promise.resolve();
    fetchMock.mockClear();
    expect(fetchMock).toHaveBeenCalledTimes(0);
    state.result = null;
    state.current_player = 1;
    rerender(<GameBoard state={state} server="http://s" gameId="1" />);
    await Promise.resolve();
  });

  it('ignores score changes', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true }));
    global.fetch = fetchMock;
    const state = mockState(0);
    const { rerender } = render(
      <GameBoard state={state} server="http://s" gameId="1" />,
    );
    await Promise.resolve();
    fetchMock.mockClear();
    state.players[0].score = 26000;
    rerender(<GameBoard state={state} server="http://s" gameId="1" />);
    await Promise.resolve();
    expect(fetchMock).toHaveBeenCalledTimes(0);
  });
});
