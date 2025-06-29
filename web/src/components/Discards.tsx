import type { Tile } from '@mymahjong/core';

export interface DiscardsProps {
  tiles: Tile[];
}

export function Discards({ tiles }: DiscardsProps): JSX.Element {
  return (
    <ul className="discards">
      {tiles.map((t, i) => (
        <li key={i}>{t.toString()}</li>
      ))}
    </ul>
  );
}
