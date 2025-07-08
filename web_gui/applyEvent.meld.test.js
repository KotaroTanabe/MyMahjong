import { describe, it, expect } from 'vitest';
import { applyEvent } from './applyEvent.js';

function baseState() {
  return {
    players: [
      { hand: { tiles: [
          { suit: 'man', value: 1 },
          { suit: 'man', value: 1 },
          { suit: 'man', value: 1 }
        ], melds: [] }, river: [] },
      { hand: { tiles: [], melds: [] }, river: [] },
      { hand: { tiles: [], melds: [] }, river: [] },
      { hand: { tiles: [], melds: [] }, river: [] },
    ],
    current_player: 0,
    last_discard: null,
    last_discard_player: null,
    waiting_for_claims: [],
  };
}

describe('applyEvent meld', () => {
  it('removes only hand tiles when processing pon', () => {
    const state = baseState();
    const event = {
      name: 'meld',
      payload: {
        player_index: 0,
        meld: {
          tiles: [
            { suit: 'man', value: 1 },
            { suit: 'man', value: 1 },
            { suit: 'man', value: 1 }
          ],
          type: 'pon',
          called_index: 2,
          called_from: 1,
        },
      },
    };
    const next = applyEvent(state, event);
    expect(next.players[0].hand.tiles.length).toBe(1);
    expect(next.players[0].hand.melds.length).toBe(1);
  });
});
