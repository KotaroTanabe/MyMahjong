import type { Tile } from '@mymahjong/core';
import { Hand } from './Hand.js';
import { Discards } from './Discards.js';
import { Melds } from './Melds.js';

export interface GameBoardProps {
  currentHand: Tile[];
  currentDiscards: Tile[];
  currentMelds?: Tile[][];
  onDiscard: (index: number) => void;
}

export function GameBoard({ currentHand, currentDiscards, currentMelds = [], onDiscard }: GameBoardProps): JSX.Element {
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
        <div className="meld-discard">
          <Melds melds={currentMelds} />
          <Discards tiles={currentDiscards} />
        </div>
        <Hand tiles={currentHand} onDiscard={onDiscard} />
      </div>
    </div>
  );
}
