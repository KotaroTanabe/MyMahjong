import { useState } from 'react';
import { Game, Tile } from '@mymahjong/core';

interface GameState {
  hand: Tile[];
  discards: Tile[];
  wallCount: number;
}

export function useGame(): GameState & {
  draw: () => Tile;
  discard: (index: number) => Tile;
} {
  const [game] = useState(() => {
    const g = new Game(1);
    g.deal();
    return g;
  });

  const [state, setState] = useState<GameState>(() => ({
    hand: [...game.players[0].hand],
    discards: [...game.players[0].discards],
    wallCount: game.wall.count,
  }));

  const sync = () => {
    setState({
      hand: [...game.players[0].hand],
      discards: [...game.players[0].discards],
      wallCount: game.wall.count,
    });
  };

  const draw = () => {
    const tile = game.drawCurrent();
    sync();
    return tile;
  };

  const discard = (index: number) => {
    const tile = game.discardCurrent(index);
    sync();
    return tile;
  };

  return { ...state, draw, discard };
}
