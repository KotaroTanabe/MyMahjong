import type { Tile } from '@mymahjong/core';
import { Hand } from './Hand.js';
import { Discards } from './Discards.js';
import { Melds } from './Melds.js';
import { TileImage } from './TileImage.js';

export interface GameBoardProps {
  currentHand: Tile[];
  /** Discard piles for all players in game order. */
  playerDiscards: Tile[][];
  /** Tiles shown in the center such as dora indicators. */
  centerTiles?: Tile[];
  currentMelds?: Tile[][];
  onDiscard: (index: number) => void;
}

export function GameBoard({ currentHand, playerDiscards, centerTiles = [], currentMelds = [], onDiscard }: GameBoardProps): JSX.Element {
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
      <div className="center">
        {centerTiles.map((t, i) => (
          <TileImage key={i} tile={t} />
        ))}
      </div>
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
      </div>
    </div>
  );
}
