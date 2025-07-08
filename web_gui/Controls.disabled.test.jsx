import { render, screen, cleanup } from '@testing-library/react';
import { describe, it, expect, afterEach } from 'vitest';
import Controls from './Controls.jsx';

afterEach(() => {
  cleanup();
});

describe('Controls disabled state', () => {
  it('disables when not active player', () => {
    render(
      <Controls
        server="http://s"
        gameId="1"
        playerIndex={0}
        activePlayer={1}
        allowedActions={['pon']}
        waitingForClaims={[]}
      />,
    );
    expect(screen.getByRole('button', { name: 'Pon' }).disabled).toBe(true);
  });
  it('disables when AI is active', () => {
    render(
      <Controls
        server="http://s"
        gameId="1"
        playerIndex={0}
        activePlayer={0}
        aiActive={true}
        allowedActions={['pon']}
        waitingForClaims={[]}
      />,
    );
    expect(screen.getByRole('button', { name: 'Pon' }).disabled).toBe(true);
  });
  it('enabled only for allowed action', () => {
    render(
      <Controls
        server="http://s"
        gameId="1"
        playerIndex={0}
        activePlayer={0}
        aiActive={false}
        allowedActions={['pon']}
        waitingForClaims={[]}
      />,
    );
    expect(screen.getByRole('button', { name: 'Pon' }).disabled).toBe(false);
    expect(screen.getByRole('button', { name: 'Chi' }).disabled).toBe(true);
  });

  it('enables controls when waiting to claim', () => {
    render(
      <Controls
        server="http://s"
        gameId="1"
        playerIndex={0}
        activePlayer={1}
        aiActive={false}
        allowedActions={['skip']}
        waitingForClaims={[0]}
      />,
    );
    expect(screen.getByRole('button', { name: 'Skip' }).disabled).toBe(false);
  });
});
