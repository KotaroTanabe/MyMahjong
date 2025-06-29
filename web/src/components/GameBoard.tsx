import type { Tile } from '@mymahjong/core';
import { Hand } from './Hand.js';
import { DiscardPile } from './DiscardPile.js';
import { Melds } from './Melds.js';

export interface GameBoardProps {
  currentHand: Tile[];
  /** Discard piles for all players in game order. */
  playerDiscards: Tile[][];
  currentMelds?: Tile[][];
  onDiscard: (index: number) => void;
}

export function GameBoard({ currentHand, playerDiscards, currentMelds = [], onDiscard }: GameBoardProps): JSX.Element {
  return (
    <div className="board">
      <div className="player-area top">
        <p>Player 2</p>
        <DiscardPile tiles={playerDiscards[1] ?? []} position="top" />
      </div>
      <div className="player-area left">
        <p>Player 3</p>
        <DiscardPile tiles={playerDiscards[2] ?? []} position="left" />
      </div>
      <div className="center">Center</div>
      <div className="player-area right">
        <p>Player 4</p>
        <DiscardPile tiles={playerDiscards[3] ?? []} position="right" />
      </div>
      <div className="player-area bottom">
        <div className="meld-discard">
          <Melds melds={currentMelds} />
          <DiscardPile tiles={playerDiscards[0] ?? []} position="bottom" />
        </div>
        <Hand tiles={currentHand} onDiscard={onDiscard} />
      </div>
    </div>
  );
}
