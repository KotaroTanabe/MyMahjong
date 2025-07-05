import React from 'react';
import Hand from './Hand.jsx';
import River from './River.jsx';
import MeldArea from './MeldArea.jsx';
import CenterDisplay from './CenterDisplay.jsx';
import Controls from './Controls.jsx';
import { tileToEmoji } from './tileUtils.js';

function tileLabel(tile) {
  return tileToEmoji(tile);
}
export default function GameBoard({ state, server, gameId }) {
  const players = state?.players ?? [];
  const south = players[0];
  const west = players[1];
  const north = players[2];
  const east = players[3];

  const nameWithRiichi = (p) => (p?.riichi ? `${p.name} (Riichi)` : p?.name);
  const defaultHand = Array(13).fill('🀫');

  const northHand = north?.hand?.tiles.map(tileLabel) ?? defaultHand;
  const westHand = west?.hand?.tiles.map(tileLabel) ?? defaultHand;
  const eastHand = east?.hand?.tiles.map(tileLabel) ?? defaultHand;
  const southHand = south?.hand?.tiles.map(tileLabel) ?? defaultHand;

  const northMelds = north?.hand?.melds.map((m) => m.tiles.map(tileLabel)) ?? [];
  const westMelds = west?.hand?.melds.map((m) => m.tiles.map(tileLabel)) ?? [];
  const eastMelds = east?.hand?.melds.map((m) => m.tiles.map(tileLabel)) ?? [];
  const southMelds = south?.hand?.melds.map((m) => m.tiles.map(tileLabel)) ?? [];

  const remaining = state?.wall?.tiles?.length ?? 0;
  const dora = state?.wall?.tiles?.[0] ? [tileLabel(state.wall.tiles[0])] : [];

  async function discard(tile) {
    try {
      if (!gameId) return;
      await fetch(`${server.replace(/\/$/, '')}/games/${gameId}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_index: 0, action: 'discard', tile }),
      });
    } catch {
      // ignore errors for now
    }
  }

  return (
    <div className="board-grid">
      <div className="north seat">
        <div>{nameWithRiichi(north) || 'North'}</div>
        <MeldArea melds={northMelds} />
        <River tiles={(north?.river ?? []).map(tileLabel)} />
        <Hand tiles={northHand} />
      </div>

      <div className="west seat">
        <div>{nameWithRiichi(west) || 'West'}</div>
        <MeldArea melds={westMelds} />
        <River tiles={(west?.river ?? []).map(tileLabel)} />
        <Hand tiles={westHand} />
      </div>

      <div className="center">
        <CenterDisplay remaining={remaining} dora={dora} />
      </div>

      <div className="east seat">
        <div>{nameWithRiichi(east) || 'East'}</div>
        <MeldArea melds={eastMelds} />
        <River tiles={(east?.river ?? []).map(tileLabel)} />
        <Hand tiles={eastHand} />
      </div>

      <div className="south seat">
        <div>{nameWithRiichi(south) || 'South'}</div>
        <MeldArea melds={southMelds} />
        <River tiles={(south?.river ?? []).map(tileLabel)} />
        <Hand tiles={southHand} onDiscard={discard} />
        <Controls server={server} gameId={gameId} />
        <MeldArea melds={southMelds} />
      </div>
    </div>
  );
}
