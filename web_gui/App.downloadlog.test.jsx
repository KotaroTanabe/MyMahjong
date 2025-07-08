import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Server } from 'mock-socket';
import { describe, it, expect, vi } from 'vitest';
import App from './App.jsx';

function fetchWithLog() {
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
    if (url.endsWith('/mjai-log')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ log: '{}' }) });
    }
    if (url.endsWith('/log')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ log: '{}' }) });
    }
    return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
  });
}

describe('Log downloads', () => {
  it('requests MJAI log when button clicked', async () => {
    const fetchMock = fetchWithLog();
    global.fetch = fetchMock;
    Object.assign(URL, { createObjectURL: vi.fn(() => 'blob:url'), revokeObjectURL: vi.fn() });
    const server = new Server('ws://localhost:1235/ws/1');
    render(<App />);
    const input = screen.getByLabelText('Server:');
    await userEvent.clear(input);
    await userEvent.type(input, 'http://localhost:1235');
    await userEvent.click(screen.getByText('Start Game'));
    await screen.findByLabelText('Options');
    const btn = await screen.findByLabelText('Download MJAI log');
    await userEvent.click(btn);
    const called = fetchMock.mock.calls.some(c => String(c[0]).includes('/mjai-log'));
    expect(called).toBe(true);
    server.stop();
  });
});
