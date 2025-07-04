import { render, screen, cleanup } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Server } from 'mock-socket';
import { describe, it, vi, expect, afterEach } from 'vitest';
import App from './App.jsx';

afterEach(() => {
  cleanup();
  localStorage.clear();
});

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

describe('App practice mode', () => {
  it('fetches a practice problem when mode is selected', async () => {
    global.fetch = vi.fn((url) => {
      if (url.endsWith('/health')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ status: 'ok' }) });
      }
      if (url.endsWith('/practice')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({
          hand: [{ suit: 'man', value: 1 }],
          dora_indicator: { suit: 'pin', value: 9 },
          seat_wind: 'east'
        }) });
      }
      if (url.endsWith('/practice/suggest')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ suit: 'man', value: 1 }) });
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    });

    render(<App />);
    const modeSelect = screen.getAllByLabelText('Mode:')[0];
    await userEvent.selectOptions(modeSelect, 'practice');
    const element = await screen.findByText('Seat wind: east');
    expect(element).toBeTruthy();
  });
});

describe('App reload', () => {
  it('restores server and game id from localStorage', async () => {
    localStorage.setItem('serverUrl', 'http://localhost:5678');
    localStorage.setItem('gameId', '1');
    global.fetch = vi.fn((url) => {
      if (url.endsWith('/health')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ status: 'ok' }) });
      }
      if (url.endsWith('/games/1')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({
          players: [],
          wall: { tiles: [] }
        }) });
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    });

    const server = new Server('ws://localhost:5678/ws/1');
    render(<App />);
    await screen.findByText('WebSocket connected');
    expect(screen.getByLabelText('Server:').value).toBe('http://localhost:5678');
    expect(screen.getByLabelText('Game ID:').value).toBe('1');
    server.stop();
  });
});
