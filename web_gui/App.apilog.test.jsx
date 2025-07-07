import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Server } from 'mock-socket';
import { describe, it, expect, vi } from 'vitest';
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
        wall: { tiles: [] }
      }) });
    }
    return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
  });
}

describe('App API logging', () => {
  it('logs start game request', async () => {
    global.fetch = mockFetch();
    const server = new Server('ws://localhost:1235/ws/1');
    render(<App />);
    const input = screen.getByLabelText('Server:');
    await userEvent.clear(input);
    await userEvent.type(input, 'http://localhost:1235');
    await userEvent.click(screen.getByText('Start Game'));
    const logItem = await screen.findByText(/\[debug\] POST \/games/);
    expect(logItem).toBeTruthy();
    server.stop();
  });
});
