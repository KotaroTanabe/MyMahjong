import { render, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import GameBoard from './GameBoard.jsx';

function stateWithResult() {
  return {
    players: new Array(4).fill(0).map(() => ({ hand: { tiles: [], melds: [] }, river: [] })),
    wall: { tiles: [] },
    result: {
      type: 'ryukyoku',
      reason: 'wall_empty',
      scores: [25000, 25000, 25000, 25000],
      tenpai: [false, false, false, false],
    },
  };
}

function blankState() {
  return {
    players: new Array(4).fill(0).map(() => ({ hand: { tiles: [], melds: [] }, river: [] })),
    wall: { tiles: [] },
  };
}

describe('GameBoard result modal', () => {
  it('persists after state update until closed', () => {
    const { rerender, getByText, getAllByLabelText, queryByText } = render(
      <GameBoard state={stateWithResult()} server="" gameId="1" />,
    );
    expect(getByText('Exhaustive draw')).toBeTruthy();
    rerender(<GameBoard state={blankState()} server="" gameId="1" />);
    expect(getByText('Exhaustive draw')).toBeTruthy();
    fireEvent.click(getAllByLabelText('close')[0]);
    expect(queryByText('Exhaustive draw')).toBeNull();
  });
});
