import { describe, it, expect, vi } from 'vitest';
import { postAction } from './postAction.js';

describe('postAction', () => {
  it('retries on 409 with next action', async () => {
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
          json: () => Promise.resolve({ player_index: 1, actions: ['draw'] }),
        });
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    });
    global.fetch = fetchMock;
    const onError = vi.fn();
    const ok = await postAction('http://s', '1', { player_index: 0, action: 'skip' }, () => {}, onError);
    expect(ok).toBe(true);
    expect(fetchMock).toHaveBeenCalledTimes(3);
    expect(onError).not.toHaveBeenCalled();
  });
});
