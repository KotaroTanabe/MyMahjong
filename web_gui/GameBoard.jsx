import React, { useEffect, useRef } from 'react';
import Hand from './Hand.jsx';
import River from './River.jsx';
import MeldArea from './MeldArea.jsx';
import CenterDisplay from './CenterDisplay.jsx';
import Controls from './Controls.jsx';
import { tileToEmoji, tileDescription } from './tileUtils.js';

function tileLabel(tile) {
  return tileToEmoji(tile);
}
export default function GameBoard({
  state,
  server,
  gameId,
  peek = false,
  layout = 'classic',
}) {
  const players = state?.players ?? [];
  const south = players[0];
  const west = players[1];
  const north = players[2];
  const east = players[3];

  const prevPlayer = useRef(null);

  useEffect(() => {
    const current = state?.current_player;
    if (!gameId || current == null || current === prevPlayer.current) return;
    prevPlayer.current = current;
    const tiles = state?.players?.[current]?.hand?.tiles ?? [];
    if (tiles.length === 13) {
      fetch(`${server.replace(/\/$/, '')}/games/${gameId}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_index: current, action: 'draw' }),
      }).catch(() => {});
    }
  }, [state?.current_player, gameId, server, state?.players]);

  const nameWithRiichi = (p) => (p?.riichi ? `${p.name} (Riichi)` : p?.name);
  const defaultHand = Array(13).fill('🀫');

  function concealedHand(p) {
    const count = p?.hand?.tiles?.length ?? 13;
    return Array(count).fill('🀫');
  }

  const northHand =
    peek ? north?.hand?.tiles.map(tileLabel) ?? defaultHand : concealedHand(north);
  const westHand =
    peek ? west?.hand?.tiles.map(tileLabel) ?? defaultHand : concealedHand(west);
  const eastHand =
    peek ? east?.hand?.tiles.map(tileLabel) ?? defaultHand : concealedHand(east);
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

  const boardClass = layout === 'classic' ? 'board-grid' : 'board-grid-alt';

  if (layout !== 'classic') {
    const panel = (p, hand, melds, riverTiles, seat, onDiscard) => (
      <div className={`${seat} seat player-panel`}>
        <div className="player-header">
          <span className="riichi-stick">{p?.riichi ? '|' : '\u00a0'}</span>
          <span>{(p ? p.name : seat) + (p ? ` ${p.score}` : '')}</span>
        </div>
        <River tiles={riverTiles} />
        <div className="hand-with-melds">
          <Hand tiles={hand} onDiscard={onDiscard} />
          <MeldArea melds={melds} />
        </div>
      </div>
    );

    return (
      <div className={boardClass}>
        {panel(north, northHand, northMelds, (north?.river ?? []).map(tileLabel), 'north')}
        {panel(east, eastHand, eastMelds, (east?.river ?? []).map(tileLabel), 'east')}
        {panel(west, westHand, westMelds, (west?.river ?? []).map(tileLabel), 'west')}
        {panel(south, southHand, southMelds, (south?.river ?? []).map(tileLabel), 'south', discard)}
      </div>
    );
  }

  return (
    <div className={boardClass}>
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
