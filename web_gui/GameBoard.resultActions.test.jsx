import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import GameBoard from './GameBoard.jsx';

function stateWithResult() {
  return {
    players: new Array(4).fill(0).map(() => ({ hand: { tiles: [], melds: [] }, river: [] })),
    wall: { tiles: [] },
    result: {
      type: 'tsumo',
      player_index: 0,
      scores: [25000, 25000, 25000, 25000],
    },
  };
}

describe('GameBoard actions cleared on result', () => {
  it('disables action buttons when result displayed', () => {
    render(<GameBoard state={stateWithResult()} server="" gameId="1" allowedActions={[['ron'], [], [], []]} />);
    const ronBtns = screen.getAllByRole('button', { name: 'Ron' });
    expect(ronBtns.every(b => b.disabled)).toBe(true);
  });
});
