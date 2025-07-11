import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import River from './River.jsx';

describe('River highlightIndex', () => {
  it('adds waiting-discard class to highlighted tile', () => {
    const { container } = render(
      <River tiles={['A', 'B']} highlightIndex={1} />,
    );
    const cells = container.querySelectorAll('.river .mj-tile');
    expect(cells[1].className).toContain('waiting-discard');
  });
});
