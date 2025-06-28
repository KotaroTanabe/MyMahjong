import type { Tile } from '@mymahjong/core';
import { Hand } from './Hand.js';

export interface GameBoardProps {
  currentHand: Tile[];
  onDiscard: (index: number) => void;
}

export function GameBoard({ currentHand, onDiscard }: GameBoardProps): JSX.Element {
  return (
    <div className="board">
      <div className="player-area top">Player 2 Hand</div>
      <div className="player-area left">Player 3 Hand</div>
      <div className="center">Center</div>
      <div className="player-area right">Player 4 Hand</div>
      <div className="player-area bottom">
        <Hand tiles={currentHand} onDiscard={onDiscard} />
      </div>
    </div>
  );
}
