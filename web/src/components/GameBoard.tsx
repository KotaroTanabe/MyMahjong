import type { Tile } from '@mymahjong/core';
import { Hand } from './Hand.js';
import { DiscardPile } from './DiscardPile.js';
import { Melds } from './Melds.js';
import { CenterDisplay } from './CenterDisplay.js';

export interface GameBoardProps {
  currentHand: Tile[];
  /** Discard piles for all players in game order. */
  playerDiscards: Tile[][];
  /** Tiles shown in the center such as dora indicators. */
  centerTiles?: Tile[];
  /** Number of tiles remaining in the wall. */
  wallCount: number;
  currentMelds?: Tile[][];
  onDiscard: (index: number) => void;
  onPon?: (fromIndex: number) => void;
  onChi?: (fromIndex: number) => void;
  onKan?: (fromIndex: number) => void;
  onRon?: (fromIndex: number) => void;
}

export function GameBoard({ currentHand, playerDiscards, centerTiles = [], wallCount, currentMelds = [], onDiscard, onPon, onChi, onKan, onRon }: GameBoardProps): JSX.Element {
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
      <CenterDisplay tiles={centerTiles} wallCount={wallCount} />
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
        <div className="meld-buttons">
          <button
            className="icon-button"
            aria-label="Pon"
            onClick={() => onPon?.(3)}
          >
            📣
          </button>
          <button
            className="icon-button"
            aria-label="Chi"
            onClick={() => onChi?.(3)}
          >
            ➡️
          </button>
          <button
            className="icon-button"
            aria-label="Kan"
            onClick={() => onKan?.(3)}
          >
            ➕
          </button>
          <button
            className="icon-button"
            aria-label="Ron"
            onClick={() => onRon?.(3)}
          >
            🚩
          </button>
        </div>
      </div>
    </div>
  );
}
