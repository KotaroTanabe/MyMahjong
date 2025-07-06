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
      state={{ players: [{}, {}, {}, {}] }}
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

describe('PlayerPanel layout styles', () => {
  it('sets river margin and hand z-index', () => {
    const { container } = render(panel(false));
    const river = container.querySelector('.river');
    const hand = container.querySelector('.hand-with-melds');
    expect(river.style.marginBottom).toBe('calc(var(--tile-font-size) * 0.8)');
    expect(hand.style.zIndex).toBe('1');
  });
});
