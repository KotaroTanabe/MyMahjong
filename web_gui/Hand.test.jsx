import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Hand from './Hand.jsx';

function renderTiles(drawn) {
  const tiles = ['A', 'B', 'C'];
  const { container } = render(<Hand tiles={tiles} drawn={drawn} />);
  return container.querySelectorAll('.mj-tile');
}

describe('Hand drawn tile spacing', () => {
  it('adds drawn-tile class when drawn is true', () => {
    const tiles = renderTiles(true);
    expect(tiles[tiles.length - 1].className).toContain('drawn-tile');
  });

  it('omits drawn-tile class when drawn is false', () => {
    const tiles = renderTiles(false);
    expect(tiles[tiles.length - 1].className).not.toContain('drawn-tile');
  });
});
