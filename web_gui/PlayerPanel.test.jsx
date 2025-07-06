import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import PlayerPanel from './PlayerPanel.jsx';

function panel(aiActive) {
  return (
    <PlayerPanel
      seat="east"
      player={{}}
      hand={[]}
      melds={[]}
      riverTiles={[]}
      server=""
      gameId="1"
      playerIndex={0}
      activePlayer={0}
      aiActive={aiActive}
    />
  );
}

describe('PlayerPanel AI button icon', () => {
  it('changes icon when aiActive toggles', () => {
    const { rerender, getByLabelText } = render(panel(false));
    const first = getByLabelText('Enable AI').innerHTML;
    rerender(panel(true));
    expect(getByLabelText('Disable AI').innerHTML).not.toBe(first);
  });
});
