import React from 'react';
import { create } from 'react-test-renderer';
import { describe, it, expect, vi } from 'vitest';
import PlayerPanel from './PlayerPanel.jsx';
import * as ControlsModule from './Controls.jsx';

const baseProps = {
  seat: 'east',
  player: {},
  hand: [],
  melds: [],
  riverTiles: [],
  server: '',
  gameId: '',
  playerIndex: 0,
  activePlayer: 0,
  aiActive: false,
  state: { players: [] },
};

describe('PlayerPanel allowedActions memoization', () => {
  it('does not re-render Controls when actions array identity changes without content change', () => {
    const spy = vi.spyOn(ControlsModule, 'Controls');
    const renderer = create(<PlayerPanel {...baseProps} allowedActions={['pon']} />);
    spy.mockClear();
    renderer.update(<PlayerPanel {...baseProps} allowedActions={['pon']} />);
    expect(spy).not.toHaveBeenCalled();
  });
});
