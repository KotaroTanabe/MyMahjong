import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Server } from 'mock-socket';
import { describe, it, vi } from 'vitest';
import App from './App.jsx';

function mockFetch() {
  return vi.fn((url) => {
    if (url.endsWith('/health')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ status: 'ok' }) });
    }
    if (url.endsWith('/games')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({
        id: 1,
        players: new Array(4).fill(0).map(() => ({ name: '', hand: { tiles: [], melds: [] }, river: [] })),
        wall: { tiles: [{ suit: 'man', value: 1 }, { suit: 'man', value: 2 }] }
      }) });
    }
    return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
  });
}

describe('App websocket', () => {
  it('updates remaining count on draw_tile event', async () => {
    global.fetch = mockFetch();
    const server = new Server('ws://localhost:1234/ws/1');
    server.on('connection', socket => {
      socket.send(JSON.stringify({
        name: 'draw_tile',
        payload: { player_index: 0, tile: { suit: 'man', value: 3 } },
      }));
    });

    render(<App />);
    const input = screen.getByLabelText('Server:');
    await userEvent.clear(input);
    await userEvent.type(input, 'http://localhost:1234');
    await userEvent.click(screen.getByText('Start Game'));

    await screen.findByText('Remaining: 1');
    server.stop();
  });
});
