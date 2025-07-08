import { describe, it, expect, vi } from 'vitest';
import { getAllowedActions, getAllAllowedActions, applyAllowedActionsEvent } from './allowedActions.js';

describe('getAllowedActions', () => {
  it('fetches server actions', async () => {
    const fetchMock = vi.fn(() =>
      Promise.resolve({ ok: true, json: () => Promise.resolve({ actions: ['pon'] }) })
    );
    global.fetch = fetchMock;
    const actions = await getAllowedActions('http://s', '1', 0, undefined, { requestId: 'a' });
    expect(fetchMock).toHaveBeenCalled();
    expect(actions).toEqual(['pon']);
  });

  it('handles fetch failure gracefully', async () => {
    const fetchMock = vi.fn(() => Promise.reject(new Error('x')));
    global.fetch = fetchMock;
    const actions = await getAllowedActions('http://s', '1', 0, undefined, { requestId: 'b' });
    expect(actions).toEqual({ error: 'x' });
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
    getAllowedActions('http://s', '1', 0, undefined, { requestId: 'x' });
    await Promise.resolve();
    getAllowedActions('http://s', '1', 0, undefined, { requestId: 'x' });
    await Promise.resolve();
    expect(aborted).toBe(true);
  });
});

describe('getAllAllowedActions', () => {
  it('fetches actions for all players', async () => {
    const fetchMock = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ actions: [['pon'], ['chi']] }),
      })
    );
    global.fetch = fetchMock;
    const actions = await getAllAllowedActions('http://s', '1', undefined, { requestId: 'all' });
    expect(fetchMock.mock.calls[0][0]).toBe('http://s/games/1/allowed-actions');
    expect(actions).toEqual([['pon'], ['chi']]);
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
    getAllAllowedActions('http://s', '1', undefined, { requestId: 'z' });
    await Promise.resolve();
    getAllAllowedActions('http://s', '1', undefined, { requestId: 'z' });
    await Promise.resolve();
    expect(aborted).toBe(true);
  });
});

describe('applyAllowedActionsEvent', () => {
  it('updates actions when event matches', () => {
    const prev = [[], [], [], []];
    const evt = { name: 'allowed_actions', payload: { actions: [['pon']] } };
    expect(applyAllowedActionsEvent(prev, evt)).toEqual([['pon']]);
  });
  it('returns current when unrelated', () => {
    const prev = [["skip"]];
    const evt = { name: 'draw_tile', payload: {} };
    expect(applyAllowedActionsEvent(prev, evt)).toBe(prev);
  });
});
