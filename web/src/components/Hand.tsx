import type { Tile } from '@mymahjong/core';

export interface HandProps {
  tiles: Tile[];
  onDiscard: (index: number) => void;
}

export function Hand({ tiles, onDiscard }: HandProps): JSX.Element {
  return (
    <ul className="hand">
      {tiles.map((tile, i) => (
        <li key={i}>
          {tile.toString()}
          <button aria-label="Discard" onClick={() => onDiscard(i)}>🗑️</button>
        </li>
      ))}
    </ul>
  );
}
