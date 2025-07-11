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
      riverTiles={[]}
      server=""
      gameId="1"
      playerIndex={1}
      activePlayer={0}
      aiActive={false}
      state={{ waiting_for_claims: waiting, players: [{}, {}, {}, {}] }}
      allowedActions={[]}
    />
  );
}

describe('PlayerPanel waiting-player class', () => {
  it('does not add waiting-player when waiting for claim', () => {
    const { container } = render(Panel([1]));
    const div = container.querySelector('.player-panel');
    expect(div.className).not.toContain('waiting-player');
  });
});
