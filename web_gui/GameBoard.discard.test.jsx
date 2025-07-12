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
    const fetchMock = vi.fn(() => Promise.resolve({ ok: false, status: 500 }));
    global.fetch = fetchMock;
    const state = { current_player: 0, players: mockPlayers(), wall: { tiles: [] } };
    render(<GameBoard state={state} server="http://s" gameId="1" />);
    await Promise.resolve();
    fetchMock.mockClear();
    const label = `Discard ${tileDescription({ suit: 'man', value: 1 })}`;
    const btn = screen.getAllByRole('button', { name: label })[0];
    await userEvent.click(btn);
    const modal = await screen.findByText('Action discard failed: 500');
    expect(modal).toBeTruthy();
  });

  it('retries on 409 conflict using next actions', async () => {
    let actionCalls = 0;
    const fetchMock = vi.fn((url) => {
      if (url.endsWith('/action')) {
        actionCalls++;
        if (actionCalls === 1) {
          return Promise.resolve({
            ok: false,
            status: 409,
            json: () => Promise.resolve({ detail: 'conflict' }),
          });
        }
        return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
      }
      if (url.endsWith('/next-actions')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ player_index: 0, actions: ['discard'] }),
        });
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    });
    global.fetch = fetchMock;
    const state = { current_player: 0, players: mockPlayers(), wall: { tiles: [] } };
    render(<GameBoard state={state} server="http://s" gameId="1" />);
    const label = `Discard ${tileDescription({ suit: 'man', value: 1 })}`;
    const btn = screen.getAllByRole('button', { name: label })[0];
    await userEvent.click(btn);
    await Promise.resolve();
    expect(fetchMock.mock.calls.some(c => c[0].includes('/next-actions'))).toBe(true);
    const lastCall = fetchMock.mock.calls.at(-1);
    expect(JSON.parse(lastCall[1].body)).toEqual({
      player_index: 0,
      action: 'discard',
    });
    // no error modal should be shown
  });
});
