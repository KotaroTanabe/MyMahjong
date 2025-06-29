import type { Tile } from '@mymahjong/core';

// Images under public/tiles are emoji-based placeholders because
// binary assets cannot be committed in this environment.

export interface TileImageProps {
  tile: Tile;
}

export function TileImage({ tile }: TileImageProps): JSX.Element {
  // During node-based tests import.meta.env is undefined, so fall back to '/'.
  const base = (import.meta as any).env?.BASE_URL ?? '/';
  const src = `${base}tiles/${tile.toString()}.svg`;
  const alt = `${tile.suit} ${tile.value}`;
  return <img src={src} alt={alt} />;
}
