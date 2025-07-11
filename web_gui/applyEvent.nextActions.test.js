import { describe, it, expect } from 'vitest';
import { applyEvent } from './applyEvent.js';

function mockState() {
  return {
    players: [],
    current_player: 0,
    waiting_for_claims: [],
  };
}

describe('applyEvent next_actions', () => {
  it('sets current player from payload', () => {
    const state = mockState();
    const evt = { name: 'next_actions', payload: { player_index: 2, actions: ['draw'] } };
    const next = applyEvent(state, evt);
    expect(next.current_player).toBe(2);
  });
});
