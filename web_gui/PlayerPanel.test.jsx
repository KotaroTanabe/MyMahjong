import { render } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
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
      allowedActions={[]}
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

describe('PlayerPanel fetch cancellation', () => {
  it('aborts previous request when props change', async () => {
    let aborted = false;
    const fetchMock = vi.fn((url, opts) => {
      opts.signal.addEventListener('abort', () => {
        aborted = true;
      });
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ actions: [] }) });
    });
    global.fetch = fetchMock;
    function Panel({ server }) {
      return (
        <PlayerPanel
          seat="east"
          player={{}}
          hand={[]}
          melds={[]}
          riverTiles={[]}
          server={server}
          gameId="1"
          playerIndex={0}
          activePlayer={0}
          aiActive={false}
          state={{}}
          allowedActions={[]}
        />
      );
    }
    const { rerender } = render(<Panel server="http://s" />);
    await Promise.resolve();
    rerender(<Panel server="http://s2" />);
    await Promise.resolve();
    expect(aborted).toBe(true);
  });
});

describe('PlayerPanel AI behaviour', () => {
  it('does not fetch actions when aiActive is true', async () => {
    const fetchMock = vi.fn(() =>
      Promise.resolve({ ok: true, json: () => Promise.resolve({ actions: [] }) })
    );
    global.fetch = fetchMock;
    render(
      <PlayerPanel
        seat="east"
        player={{}}
        hand={[]}
        melds={[]}
        riverTiles={[]}
        server="http://s"
        gameId="1"
        playerIndex={0}
        activePlayer={0}
        aiActive={true}
        state={{}}
        allowedActions={[]}
      />,
    );
    await Promise.resolve();
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
