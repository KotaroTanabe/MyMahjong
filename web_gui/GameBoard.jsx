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
export default function GameBoard({ state, server }) {
  const players = state?.players ?? [];
  const south = players[0];
  const west = players[1];
  const north = players[2];
  const east = players[3];
  const defaultHand = Array(13).fill('🀫');
  const northHand = north?.hand?.tiles.map(tileLabel) ?? defaultHand;
  const westHand = west?.hand?.tiles.map(tileLabel) ?? defaultHand;
  const eastHand = east?.hand?.tiles.map(tileLabel) ?? defaultHand;
  const southHand = south?.hand?.tiles.map(tileLabel) ?? defaultHand;

  return (
    <div className="board-grid">
      <div className="north seat">
        <div>{north?.name ?? 'North'}</div>
        <MeldArea melds={[]} />
        <River tiles={(north?.river ?? []).map(tileLabel)} />
        <Hand tiles={northHand} />
      </div>
      <div className="west seat">
        <div>{west?.name ?? 'West'}</div>
        <MeldArea melds={[]} />
        <River tiles={(west?.river ?? []).map(tileLabel)} />
        <Hand tiles={westHand} />
      </div>
      <div className="center">
        <CenterDisplay />
      </div>
      <div className="east seat">
        <div>{east?.name ?? 'East'}</div>
        <MeldArea melds={[]} />
        <River tiles={(east?.river ?? []).map(tileLabel)} />
        <Hand tiles={eastHand} />
      </div>
      <div className="south seat">
        <div>{south?.name ?? 'South'}</div>
        <River tiles={(south?.river ?? []).map(tileLabel)} />
        <Hand tiles={southHand} />
        <Controls server={server} />
        <MeldArea melds={[]} />
      </div>
    </div>
  );
}
