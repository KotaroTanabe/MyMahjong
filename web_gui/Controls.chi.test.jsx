import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import Controls from './Controls.jsx';

function mockFetch() {
  return vi.fn((url) => {
    if (url.includes('/chi-options/')) {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ options: [[{ suit: 'man', value: 3 }, { suit: 'man', value: 4 }], [{ suit: 'man', value: 4 }, { suit: 'man', value: 6 }]] }) });
    }
    return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
  });
}

describe('Controls chi modal', () => {
  it('shows modal and sends action', async () => {
    const fetchMock = mockFetch();
    global.fetch = fetchMock;
    render(
      <Controls
        server="http://s"
        gameId="1"
        playerIndex={0}
        activePlayer={0}
        allowedActions={['chi']}
        waitingForClaims={[]}
      />,
    );
    await userEvent.click(screen.getByRole('button', { name: 'Chi' }));
    expect(fetchMock).toHaveBeenCalledWith('http://s/games/1/chi-options/0');
    const opt = await screen.findByRole('button', { name: 'chi option 0' });
    await userEvent.click(opt);
    expect(fetchMock.mock.calls[1][0]).toBe('http://s/games/1/action');
    const body = JSON.parse(fetchMock.mock.calls[1][1].body);
    expect(body).toEqual({ player_index: 0, action: 'chi', tiles: [{ suit: 'man', value: 3 }, { suit: 'man', value: 4 }] });
  });
});

