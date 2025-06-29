import type { Tile } from '@mymahjong/core';
import { TileImage } from './TileImage.js';

export interface DiscardPileProps {
  tiles: Tile[];
  position: 'top' | 'bottom' | 'left' | 'right';
}

export function DiscardPile({ tiles, position }: DiscardPileProps): JSX.Element {
  return (
    <ul className={`discard-pile ${position}`}>
      {tiles.map((t, i) => (
        <li key={i}>
          <TileImage tile={t} />
        </li>
      ))}
    </ul>
  );
}
