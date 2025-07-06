import { render, screen, cleanup, waitFor } from '@testing-library/react';
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
  it('shows options button after starting a game', async () => {
    global.fetch = mockFetch();
    const server = new Server('ws://localhost:1235/ws/1');
    render(<App />);
    const input = screen.getByLabelText('Server:');
    await userEvent.clear(input);
    await userEvent.type(input, 'http://localhost:1235');
    await userEvent.click(screen.getByText('Start Game'));
    const optionsButton = await screen.findByText('Options');
    expect(optionsButton).toBeTruthy();
    server.stop();
  });
});

describe('App practice mode', () => {
  it.skip('fetches a practice problem when mode is selected', async () => {
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
    const modeSelect = screen.getByLabelText('Mode:');
    await userEvent.selectOptions(modeSelect, 'practice');
    expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/practice'));
  });
});

describe('App shanten quiz mode', () => {
  it.skip('fetches a quiz hand and checks the answer', async () => {
    global.fetch = vi.fn((url, opts) => {
      if (url.endsWith('/health')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ status: 'ok' }) });
      }
      if (url.endsWith('/shanten-quiz') && (!opts || !opts.method)) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ hand: [{ suit: 'man', value: 1 }] }) });
      }
      if (url.endsWith('/shanten-quiz/check')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ correct: true, actual: 0 }) });
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    });

    render(<App />);
    const modeSelect = screen.getAllByLabelText('Mode:')[0];
    await userEvent.selectOptions(modeSelect, 'shanten-quiz');
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/shanten-quiz'),
        undefined,
      );
    });
    const input = screen.getByLabelText('Shanten guess');
    await userEvent.type(input, '0');
    await userEvent.click(screen.getByText('Submit'));
    const result = await screen.findByText('Correct!');
    expect(result).toBeTruthy();
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
    await userEvent.click(screen.getByText('Options'));
    expect(screen.getByLabelText('Server:').value).toBe('http://localhost:5678');
    expect(screen.getByLabelText('Game ID:').value).toBe('1');
    server.stop();
  });
});

describe('App icons', () => {
  it('renders refresh icon button', () => {
    global.fetch = mockFetch();
    render(<App />);
    const refreshButton = screen.getByLabelText('Retry');
    expect(refreshButton.querySelector('svg')).toBeTruthy();
  });

  it('toggles peek icon', async () => {
    global.fetch = mockFetch();
    render(<App />);
    const peekButton = screen.getByLabelText('Toggle peek');
    const first = peekButton.innerHTML;
    await userEvent.click(peekButton);
    expect(peekButton.innerHTML).not.toBe(first);
  });
});

describe('App settings modal', () => {
  it('hides setup fields after starting game', async () => {
    global.fetch = mockFetch();
    const server = new Server('ws://localhost:1234/ws/1');
    render(<App />);
    const input = screen.getByLabelText('Server:');
    await userEvent.clear(input);
    await userEvent.type(input, 'http://localhost:1234');
    await userEvent.click(screen.getByText('Start Game'));
    const options = await screen.findByText('Options');
    expect(screen.queryByText('Start Game')).toBeNull();
    expect(options).toBeTruthy();
    await userEvent.click(options);
    expect(screen.getByLabelText('Server:')).toBeTruthy();
    server.stop();
  });
});

describe('App connection status indicator', () => {
  it('shows green check mark when server is reachable', async () => {
    global.fetch = mockFetch();
    render(<App />);
    const icon = await screen.findByLabelText('Server ok');
    expect(icon.querySelector('svg')).toBeTruthy();
  });

  it('shows error message when server is unreachable', async () => {
    global.fetch = vi.fn(() => Promise.reject(new Error('fail')));
    render(<App />);
    const msg = await screen.findByLabelText('Server error');
    expect(msg.textContent).toMatch(/Failed to contact server/);
  });
});

describe('App header', () => {
  it('does not render a heading', () => {
    global.fetch = mockFetch();
    render(<App />);
    const heading = screen.queryByRole('heading', { level: 1 });
    expect(heading).toBeNull();
  });
});
