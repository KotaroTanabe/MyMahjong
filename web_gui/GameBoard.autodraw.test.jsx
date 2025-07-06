import { render, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';

function mockState(playerIndex = 0) {
  return {
    current_player: playerIndex,
    players: new Array(4).fill(0).map(() => ({ hand: { tiles: Array(13), melds: [] }, river: [] })),
    wall: { tiles: [] },
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
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({ player_index: 0, action: 'draw' });
    state.current_player = 1;
    rerender(<GameBoard state={state} server="http://s" gameId="1" />);
    await Promise.resolve();
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(JSON.parse(fetchMock.mock.calls[1][1].body)).toEqual({ player_index: 1, action: 'auto', ai_type: 'simple' });
    fireEvent.click(getAllByLabelText('Enable AI')[0]);
    await Promise.resolve();
    state.current_player = 0;
    rerender(<GameBoard state={state} server="http://s" gameId="1" />);
    await Promise.resolve();
    expect(fetchMock).toHaveBeenCalledTimes(3);
    expect(JSON.parse(fetchMock.mock.calls[2][1].body)).toEqual({ player_index: 0, action: 'auto', ai_type: 'simple' });
  });
});
