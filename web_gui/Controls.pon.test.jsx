import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import Controls from './Controls.jsx';

function mockFetch() {
  return vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }));
}

describe('Controls pon action', () => {
  it('uses lastDiscard tile when calling pon', async () => {
    const fetchMock = mockFetch();
    global.fetch = fetchMock;
    const last = { suit: 'dragon', value: 3 };
    render(
      <Controls
        server="http://s"
        gameId="1"
        playerIndex={0}
        activePlayer={0}
        allowedActions={['pon']}
        waitingForClaims={[]}
        lastDiscard={last}
      />,
    );
    await userEvent.click(screen.getByRole('button', { name: 'Pon' }));
    expect(fetchMock).toHaveBeenCalledWith('http://s/games/1/action', expect.objectContaining({ method: 'POST' }));
    const body = JSON.parse(fetchMock.mock.calls[0][1].body);
    expect(body).toEqual({
      player_index: 0,
      action: 'pon',
      tiles: [last, last, last],
    });
  });
});
