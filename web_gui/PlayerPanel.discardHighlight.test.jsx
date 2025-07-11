import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import PlayerPanel from './PlayerPanel.jsx';

function Panel(waiting) {
  const player = { river: [{ suit: 'man', value: 1 }] };
  return (
    <PlayerPanel
      seat="south"
      player={player}
      hand={[]}
      melds={[]}
      riverTiles={['🀇']}
      server=""
      gameId="1"
      playerIndex={0}
      activePlayer={1}
      aiActive={false}
      state={{ waiting_for_claims: waiting, last_discard_player: 0, players: [player, {}, {}, {}] }}
      allowedActions={[]}
    />
  );
}

describe('PlayerPanel last discard highlight', () => {
  it('highlights last discard when waiting for claim', () => {
    const { container } = render(Panel([1]));
    const tile = container.querySelector('.river .mj-tile');
    expect(tile.className).toContain('waiting-discard');
  });
});
