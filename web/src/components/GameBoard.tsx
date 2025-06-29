import type { Tile } from '@mymahjong/core';
import { Hand } from './Hand.js';
import { Discards } from './Discards.js';

export interface GameBoardProps {
  currentHand: Tile[];
  currentDiscards: Tile[];
  onDiscard: (index: number) => void;
}

export function GameBoard({ currentHand, currentDiscards, onDiscard }: GameBoardProps): JSX.Element {
  return (
    <div className="board">
      <div className="player-area top">
        <p>Player 2</p>
        <Discards tiles={[]} />
      </div>
      <div className="player-area left">
        <p>Player 3</p>
        <Discards tiles={[]} />
      </div>
      <div className="center">Center</div>
      <div className="player-area right">
        <p>Player 4</p>
        <Discards tiles={[]} />
      </div>
      <div className="player-area bottom">
        <Hand tiles={currentHand} onDiscard={onDiscard} />
        <Discards tiles={currentDiscards} />
      </div>
    </div>
  );
}
