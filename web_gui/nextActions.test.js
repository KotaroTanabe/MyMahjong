import { describe, it, expect, vi } from 'vitest';
import { getNextActions, cleanupNextActions } from './nextActions.js';

describe('getNextActions', () => {
  it('fetches next actions', async () => {
    const fetchMock = vi.fn(() =>
      Promise.resolve({ ok: true, json: () => Promise.resolve({ player_index: 1, actions: ['draw'] }) })
    );
    global.fetch = fetchMock;
    const data = await getNextActions('http://s', '1', undefined, { requestId: 'n1' });
    expect(fetchMock).toHaveBeenCalled();
    expect(data.actions).toEqual(['draw']);
  });

  it('warns when requestId missing', async () => {
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const fetchMock = vi.fn(() =>
      Promise.resolve({ ok: true, json: () => Promise.resolve({}) })
    );
    global.fetch = fetchMock;
    await getNextActions('http://s', '1');
    expect(warn).toHaveBeenCalled();
    warn.mockRestore();
  });

  it('cleanup aborts pending controllers', async () => {
    let aborted = false;
    const fetchMock = vi.fn((url, opts) => {
      opts.signal.addEventListener('abort', () => {
        aborted = true;
      });
      return new Promise(() => {});
    });
    global.fetch = fetchMock;
    getNextActions('http://s', '1', undefined, { requestId: 'n2' });
    await Promise.resolve();
    cleanupNextActions();
    expect(aborted).toBe(true);
  });
});
