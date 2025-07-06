import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import CenterDisplay from './CenterDisplay.jsx';

describe('CenterDisplay', () => {
  it('shows honba and riichi stick counts', () => {
    render(<CenterDisplay remaining={10} dora={[]} honba={3} riichiSticks={2} />);
    expect(screen.getByText('Remaining: 10')).toBeTruthy();
    expect(screen.getByText(/Honba: 3/)).toBeTruthy();
    expect(screen.getByText(/Riichi: 2/)).toBeTruthy();
  });
});
