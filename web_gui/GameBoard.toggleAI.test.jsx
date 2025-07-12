import { render, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';

function mockState(count = 13) {
  const tiles = Array(count).fill({ suit: 'man', value: 1 });
  return {
    current_player: 0,
    players: [
      { hand: { tiles, melds: [] }, river: [] },
      { hand: { tiles: Array(13), melds: [] }, river: [] },
      { hand: { tiles: Array(13), melds: [] }, river: [] },
      { hand: { tiles: Array(13), melds: [] }, river: [] },
    ],
    wall: { tiles: [] },
  };
}

describe('GameBoard AI toggle mid-turn', () => {
  it('discards immediately when enabling AI', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true }));
    global.fetch = fetchMock;
    const state = mockState();
    const { getAllByLabelText, rerender } = render(
      <GameBoard
        state={state}
        server="http://s"
        gameId="1"
        allowedActions={[['draw'], [], [], []]}
      />,
    );
    await Promise.resolve();
    fetchMock.mockClear();
    // simulate draw
    rerender(
      <GameBoard
        state={mockState(14)}
        server="http://s"
        gameId="1"
        allowedActions={[['discard'], [], [], []]}
      />,
    );
    await Promise.resolve();
    fireEvent.click(getAllByLabelText('Enable AI')[0]);
    await Promise.resolve();
    expect(fetchMock.mock.calls.filter(c => c[1] && c[1].body).length).toBe(1);
    expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({
      player_index: 0,
      action: 'auto',
      ai_type: 'simple',
    });
  });
});
