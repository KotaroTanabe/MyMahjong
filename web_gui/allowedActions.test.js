import { describe, it, expect } from 'vitest';
import { getAllowedActions } from './allowedActions.js';

function mockState() {
  return {
    current_player: 0,
    last_discard: { suit: 'man', value: 2 },
    last_discard_player: 1,
    players: [
      {},
      {},
      { hand: { tiles: [{ suit: 'man', value: 1 }, { suit: 'man', value: 3 }] } },
      {},
    ],
  };
}

describe('getAllowedActions', () => {
  it('allows chi when sequence exists', () => {
    const actions = getAllowedActions(mockState(), 2);
    expect(actions).toContain('chi');
  });

  it('omits pon when tiles missing', () => {
    const actions = getAllowedActions(mockState(), 2);
    expect(actions).not.toContain('pon');
  });
});
