import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import PlayerPanel from './PlayerPanel.jsx';

function Panel(waiting) {
  return (
    <PlayerPanel
      seat="east"
      player={{}}
      hand={[]}
      melds={[]}
      riverTiles={["A"]}
      server=""
      gameId="1"
      playerIndex={1}
      activePlayer={0}
      aiActive={false}
      state={{
        waiting_for_claims: waiting,
        last_discard_player: 1,
        last_discard: { suit: 'man', value: 1 },
        players: [{}, {}, {}, {}],
      }}
      allowedActions={[]}
    />
  );
}

describe('PlayerPanel waiting discard highlight', () => {
  it('highlights last discard when waiting for claim', () => {
    const { container } = render(Panel([1]));
    const tile = container.querySelector('.river .waiting-discard');
    expect(tile).not.toBeNull();
  });
});
