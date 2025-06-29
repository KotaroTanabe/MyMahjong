import { useState } from 'react';
import { Game, Tile, ScoreResult } from '@mymahjong/core';

interface GameState {
  hand: Tile[];
  discards: Tile[];
  /**
   * Discards for every player in the order they appear in the Game instance.
   * The first entry corresponds to the local player.
   */
  playerDiscards: Tile[][];
  melds: Tile[][];
  wallCount: number;
  score: ScoreResult;
}

export function useGame(game?: Game): GameState & {
  draw: () => Tile;
  discard: (index: number) => Tile;
  pon: (fromIndex: number) => void;
  chi: (fromIndex: number) => void;
  kan: (fromIndex: number) => void;
  ron: (fromIndex: number) => boolean;
} {
  const [gameInstance] = useState(() => {
    const g = game ?? new Game(1);
    if (g.players[0].hand.length === 0) {
      g.deal();
    }
    return g;
  });

  const [state, setState] = useState<GameState>(() => ({
    hand: [...gameInstance.players[0].hand],
    discards: [...gameInstance.players[0].discards],
    playerDiscards: gameInstance.players.map(p => [...p.discards]),
    melds: gameInstance.players[0].melds.map(m => [...m]),
    wallCount: gameInstance.wall.count,
    score: gameInstance.calculateScore(0),
  }));

  const sync = () => {
    setState({
      hand: [...gameInstance.players[0].hand],
      discards: [...gameInstance.players[0].discards],
      playerDiscards: gameInstance.players.map(p => [...p.discards]),
      melds: gameInstance.players[0].melds.map(m => [...m]),
      wallCount: gameInstance.wall.count,
      score: gameInstance.calculateScore(0),
    });
  };

  const draw = () => {
    const tile = gameInstance.drawCurrent();
    sync();
    return tile;
  };

  const discard = (index: number) => {
    const tile = gameInstance.discardCurrent(index);
    sync();
    return tile;
  };

  const pon = (fromIndex: number) => {
    gameInstance.callPon(0, fromIndex);
    sync();
  };

  const chi = (fromIndex: number) => {
    gameInstance.callChi(0, fromIndex);
    sync();
  };

  const kan = (fromIndex: number) => {
    gameInstance.callKan(0, fromIndex);
    sync();
  };

  const ron = (fromIndex: number) => {
    const result = gameInstance.declareRon(0, fromIndex);
    sync();
    return result;
  };

  return { ...state, draw, discard, pon, chi, kan, ron };
}
