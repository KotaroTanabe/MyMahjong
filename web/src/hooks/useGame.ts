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
  wallCount: number;
  doraIndicators: Tile[];
  score: ScoreResult;
  scoreboard: { wind: import('@mymahjong/core').Wind; points: number }[];
}

export function useGame(game?: Game): GameState & {
  draw: () => Tile;
  discard: (index: number) => Tile;
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
    wallCount: gameInstance.wall.count,
    doraIndicators: [...gameInstance.doraIndicators],
    score: gameInstance.calculateScore(0),
    scoreboard: gameInstance.players.map((p, i) => ({
      wind: p.seatWind!,
      points: gameInstance.calculateScore(i).points,
    })),
  }));

  const sync = () => {
    setState({
      hand: [...gameInstance.players[0].hand],
      discards: [...gameInstance.players[0].discards],
      playerDiscards: gameInstance.players.map(p => [...p.discards]),
      wallCount: gameInstance.wall.count,
      doraIndicators: [...gameInstance.doraIndicators],
      score: gameInstance.calculateScore(0),
      scoreboard: gameInstance.players.map((p, i) => ({
        wind: p.seatWind!,
        points: gameInstance.calculateScore(i).points,
      })),
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

  return { ...state, draw, discard };
}
