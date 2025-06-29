import type { Tile } from '@mymahjong/core';

export interface MeldsProps {
  melds: Tile[][];
}

export function Melds({ melds }: MeldsProps): JSX.Element {
  return (
    <ul className="melds">
      {melds.map((set, i) => (
        <li key={i}>{set.map(t => t.toString()).join(' ')}</li>
      ))}
    </ul>
  );
}
