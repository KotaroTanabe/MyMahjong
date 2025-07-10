import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import GameBoard from './GameBoard.jsx';
import { tileDescription } from './tileUtils.js';

function mockPlayers() {
  return new Array(4).fill(0).map(() => ({
    hand: { tiles: new Array(14).fill(0).map(() => ({ suit: 'man', value: 1 })), melds: [] },
    river: [],
  }));
}

describe('GameBoard riichi discard', () => {
  it('sends riichi when selecting tile after button', async () => {
    const fetchMock = vi.fn(url => {
      if (url.includes('/allowed-actions/0')) {
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ actions: ['riichi'] }) });
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    });
    global.fetch = fetchMock;
    const state = { current_player: 0, players: mockPlayers(), wall: { tiles: [] } };
    render(
      <GameBoard
        state={state}
        server="http://s"
        gameId="1"
        allowedActions={[['riichi'], [], [], []]}
      />,
    );
    await Promise.resolve();
    fetchMock.mockClear();
    const controls = document.querySelector('.south .controls');
    await userEvent.click(within(controls).getByRole('button', { name: 'Riichi' }));
    await new Promise(r => setTimeout(r, 0));
    const label = `Discard ${tileDescription({ suit: 'man', value: 1 })}`;
    const hand = document.querySelector('.south .hand');
    const btn = within(hand).getAllByRole('button', { name: label })[0];
    await userEvent.click(btn);
    const actionCalls = fetchMock.mock.calls.filter(c => c[0].includes('/action'));
    console.log('actions', actionCalls.map(c => ({url:c[0], body:c[1].body}))); 
    const body = JSON.parse(actionCalls[actionCalls.length - 1][1].body);
    expect(body).toEqual({
      player_index: 0,
      action: 'riichi',
      tile: { suit: 'man', value: 1 },
    });
  });
});
