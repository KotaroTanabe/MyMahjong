import { describe, it, expect, vi } from 'vitest';
import { getAllowedActions } from './allowedActions.js';

// Minimal fetch mocking

describe('getAllowedActions', () => {
  it('returns actions from server', async () => {
    const fake = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ actions: ['chi'] }),
    });
    global.fetch = fake;
    const actions = await getAllowedActions('http://s', '1', 0);
    expect(fake).toHaveBeenCalled();
    expect(actions).toEqual(['chi']);
  });
});
