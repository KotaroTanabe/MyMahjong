import { describe, it, expect, vi } from 'vitest';
import { getAllowedActions } from './allowedActions.js';

describe('getAllowedActions', () => {
  it('fetches server actions', async () => {
    const fetchMock = vi.fn(() =>
      Promise.resolve({ ok: true, json: () => Promise.resolve({ actions: ['pon'] }) })
    );
    global.fetch = fetchMock;
    const actions = await getAllowedActions('http://s', '1', 0);
    expect(fetchMock).toHaveBeenCalled();
    expect(actions).toEqual(['pon']);
  });

  it('handles fetch failure gracefully', async () => {
    const fetchMock = vi.fn(() => Promise.reject(new Error('x')));
    global.fetch = fetchMock;
    const actions = await getAllowedActions('http://s', '1', 0);
    expect(actions).toEqual([]);
  });
});
