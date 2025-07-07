import { describe, it, expect, vi } from 'vitest';
import { logNextActions } from './eventFlow.js';

describe('logNextActions', () => {
  it('fetches and logs next actions', async () => {
    const fetchMock = vi.fn(() =>
      Promise.resolve({ ok: true, json: () => Promise.resolve({ player_index: 1, actions: ['draw'] }) }),
    );
    global.fetch = fetchMock;
    const events = [];
    const log = vi.fn((l, m) => events.push(`[${l}] ${m}`));
    await logNextActions('http://s', '1', log, (line) => events.push(line));
    expect(fetchMock).toHaveBeenCalledWith('http://s/games/1/next-actions');
    expect(events.pop()).toContain('next_actions');
  });
});
