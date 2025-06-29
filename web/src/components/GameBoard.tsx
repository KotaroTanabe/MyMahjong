import type { Tile } from '@mymahjong/core';
import { Hand } from './Hand.js';
import { DiscardPile } from './DiscardPile.js';
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
        <DiscardPile tiles={[]} position="top" />
      </div>
      <div className="player-area left">
        <p>Player 3</p>
        <DiscardPile tiles={[]} position="left" />
      </div>
      <div className="center">Center</div>
      <div className="player-area right">
        <p>Player 4</p>
        <DiscardPile tiles={[]} position="right" />
      </div>
      <div className="player-area bottom">
        <div className="meld-discard">
          <Melds melds={currentMelds} />
          <DiscardPile tiles={currentDiscards} position="bottom" />
        </div>
        <Hand tiles={currentHand} onDiscard={onDiscard} />
      </div>
    </div>
  );
}
