import type { Tile } from '@mymahjong/core';
import { TileImage } from './TileImage.js';

export interface MeldsProps {
  melds: Tile[][];
}

export function Melds({ melds }: MeldsProps): JSX.Element {
  return (
    <ul className="melds">
      {melds.map((set, i) => (
        <li key={i}>
          {set.map((t, j) => (
            <TileImage key={j} tile={t} />
          ))}
        </li>
      ))}
    </ul>
  );
}
