import { render, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';

function startState() {
  const tiles = Array(14).fill({ suit: 'man', value: 1 });
  return {
    current_player: 0,
    players: [
      { hand: { tiles, melds: [] }, river: [] },
      { hand: { tiles: Array(13), melds: [] }, river: [] },
      { hand: { tiles: Array(13), melds: [] }, river: [] },
      { hand: { tiles: Array(13), melds: [] }, river: [] },
    ],
    wall: { tiles: [] },
    last_discard: null,
  };
}

describe('GameBoard initial dealer turn', () => {
  it('does not auto discard before draw event', async () => {
    const fetchMock = vi.fn(() => Promise.resolve({ ok: true }));
    global.fetch = fetchMock;
    const state = startState();
    const { getAllByLabelText } = render(
      <GameBoard state={state} server="http://s" gameId="1" />,
    );
    await Promise.resolve();
    fireEvent.click(getAllByLabelText('Enable AI')[0]);
    await Promise.resolve();
    const bodies = fetchMock.mock.calls
      .filter(c => c[1] && c[1].body)
      .map(c => JSON.parse(c[1].body));
    expect(bodies.length).toBe(0);
  });
});
