import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import ErrorModal from './ErrorModal.jsx';

describe('ErrorModal retry', () => {
  it('calls retry and close on click', async () => {
    const onClose = vi.fn();
    const onRetry = vi.fn();
    render(<ErrorModal message="oops" onClose={onClose} onRetry={onRetry} />);
    const btn = screen.getByLabelText('Retry');
    expect(btn.querySelector('svg')).toBeTruthy();
    await userEvent.click(btn);
    expect(onRetry).toHaveBeenCalled();
    expect(onClose).toHaveBeenCalled();
  });
});
