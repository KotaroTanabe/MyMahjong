import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import GameBoard from './GameBoard.jsx';

const sampleState = {
  players: [
    { name: 'South', hand: { tiles: [{ suit: 'man', value: 1 }], melds: [] }, river: [] },
    { name: 'West', hand: { tiles: [{ suit: 'man', value: 2 }], melds: [] }, river: [] },
    { name: 'North', hand: { tiles: [{ suit: 'man', value: 3 }], melds: [] }, river: [] },
    { name: 'East', hand: { tiles: [{ suit: 'man', value: 4 }], melds: [] }, river: [] },
  ],
  wall: { tiles: [] },
};

describe('GameBoard peek option', () => {
  it('hides opponent hands by default', () => {
    render(<GameBoard state={sampleState} server="" />);
    expect(screen.getAllByText('🀫').length).toBeGreaterThan(0);
    expect(screen.queryByText('🀈')).toBeNull();
  });

  it('shows opponent hands when peek is enabled', () => {
    render(<GameBoard state={sampleState} server="" peek={true} />);
    expect(screen.getByText('🀈')).toBeDefined();
  });
});
