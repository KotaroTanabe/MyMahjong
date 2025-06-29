import type { Tile } from '@mymahjong/core';
import { TileImage } from './TileImage.js';

export interface CenterDisplayProps {
  /** Tiles shown in the center such as dora indicators. */
  tiles: Tile[];
  /** Number of tiles remaining in the wall. */
  wallCount: number;
}

export function CenterDisplay({ tiles, wallCount }: CenterDisplayProps): JSX.Element {
  return (
    <div className="center">
      <div className="dora-indicators">
        {tiles.map((t, i) => (
          <TileImage key={i} tile={t} />
        ))}
      </div>
      <p className="wall-count" aria-label="Tiles left">
        {wallCount}
      </p>
    </div>
  );
}
