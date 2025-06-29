import type { Tile } from '@mymahjong/core';
import { TileImage } from './TileImage.js';

export interface DiscardsProps {
  tiles: Tile[];
}

export function Discards({ tiles }: DiscardsProps): JSX.Element {
  return (
    <ul className="discards">
      {tiles.map((t, i) => (
        <li key={i}>
          <TileImage tile={t} />
        </li>
      ))}
    </ul>
  );
}
