import { render, screen, cleanup } from '@testing-library/react';
import { describe, it, expect, afterEach } from 'vitest';
import Controls from './Controls.jsx';

afterEach(() => {
  cleanup();
});

describe('Controls disabled state', () => {
  it('disables when not active player', () => {
    render(<Controls server="http://s" gameId="1" playerIndex={0} activePlayer={1} />);
    expect(screen.getByRole('button', { name: 'Pon' }).disabled).toBe(true);
  });
  it('disables when AI is active', () => {
    render(<Controls server="http://s" gameId="1" playerIndex={0} activePlayer={0} aiActive={true} />);
    expect(screen.getByRole('button', { name: 'Pon' }).disabled).toBe(true);
  });
  it('enabled for active human', () => {
    render(<Controls server="http://s" gameId="1" playerIndex={0} activePlayer={0} aiActive={false} />);
    expect(screen.getByRole('button', { name: 'Pon' }).disabled).toBe(false);
  });
});
