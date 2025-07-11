import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';
import { tileDescription } from './tileUtils.js';

function mockPlayers() {
  return new Array(4).fill(0).map(() => ({
    hand: { tiles: [{ suit: 'man', value: 1 }], melds: [] },
    river: [],
  }));
}

describe('GameBoard discard', () => {
  it('sends discard when clicking tile on turn', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }));
    global.fetch = fetchMock;
    const state = { current_player: 0, players: mockPlayers(), wall: { tiles: [] } };
    render(<GameBoard state={state} server="http://s" gameId="1" />);
    await Promise.resolve();
    fetchMock.mockClear();
    const label = `Discard ${tileDescription({ suit: 'man', value: 1 })}`;
    const btn = screen.getAllByRole('button', { name: label })[0];
    await userEvent.click(btn);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({ player_index: 0, action: 'discard', tile: { suit: 'man', value: 1 } });
  });

  it('ignores click when not your turn', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }));
    global.fetch = fetchMock;
    const state = { current_player: 1, players: mockPlayers(), wall: { tiles: [] } };
    const { container } = render(<GameBoard state={state} server="http://s" gameId="1" />);
    await Promise.resolve();
    fetchMock.mockClear();
    const btn = container.querySelector('.south .hand button');
    expect(btn).toBeNull();
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('shows modal on server error', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: false, status: 409 }));
    global.fetch = fetchMock;
    const state = { current_player: 0, players: mockPlayers(), wall: { tiles: [] } };
    render(<GameBoard state={state} server="http://s" gameId="1" />);
    const label = `Discard ${tileDescription({ suit: 'man', value: 1 })}`;
    const btn = screen.getAllByRole('button', { name: label })[0];
    await userEvent.click(btn);
    const modal = await screen.findByText('Discard failed: 409');
    expect(modal).toBeTruthy();
  });
  it('shows server detail on conflict', async () => {
    const fetchMock = vi.fn(() =>
      Promise.resolve({
        ok: false,
        status: 409,
        json: () => Promise.resolve({ detail: 'Action not allowed' }),
      })
    );
    global.fetch = fetchMock;
    const state = { current_player: 0, players: mockPlayers(), wall: { tiles: [] } };
    render(<GameBoard state={state} server="http://s" gameId="1" />);
    const label = `Discard ${tileDescription({ suit: 'man', value: 1 })}`;
    const btn = screen.getAllByRole('button', { name: label })[0];
    await userEvent.click(btn);
    const modal = await screen.findByText(/Action not allowed/);
    expect(modal).toBeTruthy();
  });
});
