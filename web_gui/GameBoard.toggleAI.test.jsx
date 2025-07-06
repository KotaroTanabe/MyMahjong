import { render, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';

function setupFetch() {
  const fetchMock = vi.fn(() => Promise.resolve({ ok: true }));
  global.fetch = (url, options) => {
    if (String(url).includes('allowed-actions')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ actions: [] }) });
    }
    return fetchMock(url, options);
  };
  return fetchMock;
}

function mockState() {
  // player 0 has already drawn a tile (14 tiles total)
  const tiles = Array(14).fill({ suit: 'man', value: 1 });
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
    const fetchMock = setupFetch();
    const state = mockState();
    const { getAllByLabelText } = render(
      <GameBoard state={state} server="http://s" gameId="1" />,
    );
    // no request on mount because hand has 14 tiles
    expect(fetchMock).toHaveBeenCalledTimes(0);
    fireEvent.click(getAllByLabelText('Enable AI')[0]);
    await Promise.resolve();
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({
      player_index: 0,
      action: 'discard',
      tile: { suit: 'man', value: 1 },
    });
  });
});
