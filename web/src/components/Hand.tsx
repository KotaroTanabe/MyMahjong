import type { Tile } from '@mymahjong/core';
import { TileImage } from './TileImage.js';

export interface HandProps {
  tiles: Tile[];
  onDiscard: (index: number) => void;
}

export function Hand({ tiles, onDiscard }: HandProps): JSX.Element {
  return (
    <ul className="hand">
      {tiles.map((tile, i) => (
        <li key={i}>
          <TileImage tile={tile} />
          <button aria-label="Discard" onClick={() => onDiscard(i)}>🗑️</button>
        </li>
      ))}
    </ul>
  );
}
