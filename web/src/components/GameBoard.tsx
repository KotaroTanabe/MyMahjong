import type { Tile } from '@mymahjong/core';
import { Hand } from './Hand.js';
import { Discards } from './Discards.js';
import { Melds } from './Melds.js';

export interface GameBoardProps {
  currentHand: Tile[];
  /** Discard piles for all players in game order. */
  playerDiscards: Tile[][];
  currentMelds?: Tile[][];
  onDiscard: (index: number) => void;
  onPon?: (fromIndex: number) => void;
  onChi?: (fromIndex: number) => void;
  onKan?: (fromIndex: number) => void;
  onRon?: (fromIndex: number) => void;
}

export function GameBoard({ currentHand, playerDiscards, currentMelds = [], onDiscard, onPon, onChi, onKan, onRon }: GameBoardProps): JSX.Element {
  return (
    <div className="board">
      <div className="player-area top">
        <p>Player 2</p>
        <Discards tiles={playerDiscards[1] ?? []} />
      </div>
      <div className="player-area left">
        <p>Player 3</p>
        <Discards tiles={playerDiscards[2] ?? []} />
      </div>
      <div className="center">Center</div>
      <div className="player-area right">
        <p>Player 4</p>
        <Discards tiles={playerDiscards[3] ?? []} />
      </div>
      <div className="player-area bottom">
        <div className="meld-discard">
          <Melds melds={currentMelds} />
          <Discards tiles={playerDiscards[0] ?? []} />
        </div>
        <Hand tiles={currentHand} onDiscard={onDiscard} />
        <div className="meld-buttons">
          <button onClick={() => onPon?.(3)}>Pon</button>
          <button onClick={() => onChi?.(3)}>Chi</button>
          <button onClick={() => onKan?.(3)}>Kan</button>
          <button onClick={() => onRon?.(3)}>Ron</button>
        </div>
      </div>
    </div>
  );
}
