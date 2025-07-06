import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import River from './River.jsx';

describe('River layout', () => {
  it('reserves 24 grid cells', () => {
    const { container } = render(<River tiles={['A', 'B']} />);
    const cells = container.querySelectorAll('.river .tile');
    expect(cells).toHaveLength(24);
    expect(cells[0].textContent).toBe('A');
    expect(cells[1].textContent).toBe('B');
  });
});
