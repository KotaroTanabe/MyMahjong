import type { Tile } from '@mymahjong/core';
import { TileImage } from './TileImage.js';

export interface DiscardPileProps {
  tiles: Tile[];
  position?: 'top' | 'bottom' | 'left' | 'right';
}

export function DiscardPile({ tiles, position }: DiscardPileProps): JSX.Element {
  const rows: Tile[][] = [];
  for (let i = 0; i < tiles.length; i += 6) {
    rows.push(tiles.slice(i, i + 6));
  }
  return (
    <div className={`discard-pile${position ? ` ${position}` : ''}`}>
      {rows.map((row, rowIndex) => (
        <ul key={rowIndex} className="discard-row">
          {row.map((t, i) => (
            <li key={i}>
              <TileImage tile={t} />
            </li>
          ))}
        </ul>
      ))}
    </div>
  );
}
