import { describe, it, expect, vi } from 'vitest';
import { logNextActions, logClaims } from './eventFlow.js';

describe('logNextActions', () => {
  it('fetches and logs next actions', async () => {
    const fetchMock = vi.fn(() =>
      Promise.resolve({ ok: true, json: () => Promise.resolve({ player_index: 1, actions: ['draw'] }) }),
    );
    global.fetch = fetchMock;
    const events = [];
    const log = vi.fn((l, m) => events.push(`[${l}] ${m}`));
    await logNextActions('http://s', '1', log, (line) => events.push(line), { requestId: 'n' });
    expect(fetchMock.mock.calls[0][0]).toBe('http://s/games/1/next-actions');
    expect(events.pop()).toContain('next_actions');
  });

  it('aborts previous request with same id', async () => {
    let aborted = false;
    const fetchMock = vi.fn((url, opts) => {
      opts.signal.addEventListener('abort', () => {
        aborted = true;
      });
      return new Promise(() => {});
    });
    global.fetch = fetchMock;
    logNextActions('http://s', '1', () => {}, () => {}, { requestId: 'n' });
    await Promise.resolve();
    logNextActions('http://s', '1', () => {}, () => {}, { requestId: 'n' });
    await Promise.resolve();
    expect(aborted).toBe(true);
  });
});

describe('logClaims', () => {
  it('fetches and logs claim options', async () => {
    const fetchMock = vi.fn(() =>
      Promise.resolve({ ok: true, json: () => Promise.resolve({ claims: [] }) })
    );
    global.fetch = fetchMock;
    const events = [];
    const log = vi.fn((l, m) => events.push(`[${l}] ${m}`));
    await logClaims('http://s', '1', log, (line) => events.push(line), { requestId: 'c' });
    expect(fetchMock.mock.calls[0][0]).toBe('http://s/games/1/claims');
    expect(events.pop()).toContain('claims');
  });
});
