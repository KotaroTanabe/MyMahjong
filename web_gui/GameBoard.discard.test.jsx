import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';
import { tileDescription } from './tileUtils.js';

function setupFetch() {
  const fetchMock = vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }));
  global.fetch = (url, options) => {
    if (String(url).includes('allowed-actions')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ actions: [] }) });
    }
    return fetchMock(url, options);
  };
  return fetchMock;
}

function mockPlayers() {
  return new Array(4).fill(0).map(() => ({
    hand: { tiles: [{ suit: 'man', value: 1 }], melds: [] },
    river: [],
  }));
}

describe('GameBoard discard', () => {
  it('sends discard when clicking tile on turn', async () => {
    const fetchMock = setupFetch();
    const state = { current_player: 0, players: mockPlayers(), wall: { tiles: [] } };
    render(<GameBoard state={state} server="http://s" gameId="1" />);
    const label = `Discard ${tileDescription({ suit: 'man', value: 1 })}`;
    const btn = screen.getAllByRole('button', { name: label })[0];
    await userEvent.click(btn);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({ player_index: 0, action: 'discard', tile: { suit: 'man', value: 1 } });
  });

  it('ignores click when not your turn', async () => {
    const fetchMock = setupFetch();
    const state = { current_player: 1, players: mockPlayers(), wall: { tiles: [] } };
    const { container } = render(<GameBoard state={state} server="http://s" gameId="1" />);
    const btn = container.querySelector('.south .hand button');
    expect(btn).toBeNull();
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('shows modal on server error', async () => {
    const fetchMock = setupFetch();
    fetchMock.mockResolvedValueOnce({ ok: false, status: 409 });
    const state = { current_player: 0, players: mockPlayers(), wall: { tiles: [] } };
    render(<GameBoard state={state} server="http://s" gameId="1" />);
    const label = `Discard ${tileDescription({ suit: 'man', value: 1 })}`;
    const btn = screen.getAllByRole('button', { name: label })[0];
    await userEvent.click(btn);
    const modal = await screen.findByText('Discard failed: 409');
    expect(modal).toBeTruthy();
  });
});
