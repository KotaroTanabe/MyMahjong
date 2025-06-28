import React from 'react';
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
          <button onClick={() => onDiscard(i)}>Discard</button>
        </li>
      ))}
    </ul>
  );
}
