import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Server } from 'mock-socket';
import { describe, it, vi } from 'vitest';
import App from './App.jsx';
import { tileToEmoji } from './tileUtils.js';

function mockFetch() {
  return vi.fn((url) => {
    if (url.endsWith('/health')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ status: 'ok' }) });
    }
    if (url.endsWith('/games')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({
        players: new Array(4).fill(0).map(() => ({ name: '', hand: { tiles: [], melds: [] }, river: [] })),
        wall: { tiles: [] }
      }) });
    }
    return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
  });
}

describe('App start_kyoku event', () => {
  it('resets state from event payload', async () => {
    global.fetch = mockFetch();
    const server = new Server('ws://localhost:1234/ws/1');
    const tile = { suit: 'man', value: 1 };
    server.on('connection', (socket) => {
      socket.send(JSON.stringify({
        name: 'start_kyoku',
        payload: {
          state: {
            players: new Array(4).fill(0).map(() => ({
              name: '',
              hand: { tiles: [tile], melds: [] },
              river: [],
            })),
            wall: { tiles: [tile, tile, tile, tile, tile] },
          },
        },
      }));
    });

    render(<App />);
    const input = screen.getByLabelText('Server:');
    await userEvent.clear(input);
    await userEvent.type(input, 'http://localhost:1234');
    await userEvent.click(screen.getByText('Start Game'));

    await screen.findByText('Remaining: 5');
    await screen.findAllByText(tileToEmoji(tile));
    server.stop();
  });
});

