import React from 'react';
import { create } from 'react-test-renderer';
import { describe, it, expect, vi } from 'vitest';
import * as ControlsModule from './Controls.jsx';

function renderControls(props) {
  return <ControlsModule.default server="" gameId="1" {...props} />;
}

describe('Controls memoization', () => {
  it('does not re-render when props are unchanged', () => {
    const spy = vi.spyOn(ControlsModule, 'Controls');
    const testRenderer = create(renderControls({ allowedActions: ['pon'] }));
    spy.mockClear();
    testRenderer.update(renderControls({ allowedActions: ['pon'] }));
    expect(spy).not.toHaveBeenCalled();
  });
});
