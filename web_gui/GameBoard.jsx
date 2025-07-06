import React, { useEffect, useRef } from 'react';
import CenterDisplay from './CenterDisplay.jsx';
import PlayerPanel from './PlayerPanel.jsx';
import { tileToEmoji } from './tileUtils.js';

function tileLabel(tile) {
  return tileToEmoji(tile);
}
export default function GameBoard({
  state,
  server,
  gameId,
  peek = false,
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
  const southHand = south?.hand?.tiles ?? defaultHand;

  const northMelds = north?.hand?.melds.map((m) => m.tiles.map(tileLabel)) ?? [];
  const westMelds = west?.hand?.melds.map((m) => m.tiles.map(tileLabel)) ?? [];
  const eastMelds = east?.hand?.melds.map((m) => m.tiles.map(tileLabel)) ?? [];
  const southMelds = south?.hand?.melds.map((m) => m.tiles.map(tileLabel)) ?? [];

  const remaining = state?.wall?.tiles?.length ?? 0;
  const dora = state?.wall?.tiles?.[0] ? [tileLabel(state.wall.tiles[0])] : [];

  async function discard(tile) {
    try {
      if (!gameId) return;
      if (typeof tile === 'string') return;
      await fetch(`${server.replace(/\/$/, '')}/games/${gameId}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_index: 0, action: 'discard', tile }),
      });
    } catch {
      // ignore errors for now
    }
  }

  const boardClass = 'board-grid';

  return (
    <>
      <CenterDisplay remaining={remaining} dora={dora} />
      <div className={boardClass}>
      <PlayerPanel
        seat="north"
        player={north}
        hand={northHand}
        melds={northMelds}
        riverTiles={(north?.river ?? []).map(tileLabel)}
        server={server}
        gameId={gameId}
        playerIndex={2}
        activePlayer={state?.current_player}
      />
      <PlayerPanel
        seat="west"
        player={west}
        hand={westHand}
        melds={westMelds}
        riverTiles={(west?.river ?? []).map(tileLabel)}
        server={server}
        gameId={gameId}
        playerIndex={1}
        activePlayer={state?.current_player}
      />
      <PlayerPanel
        seat="east"
        player={east}
        hand={eastHand}
        melds={eastMelds}
        riverTiles={(east?.river ?? []).map(tileLabel)}
        server={server}
        gameId={gameId}
        playerIndex={3}
        activePlayer={state?.current_player}
      />
      <PlayerPanel
        seat="south"
        player={south}
        hand={southHand}
        melds={southMelds}
        riverTiles={(south?.river ?? []).map(tileLabel)}
        onDiscard={state?.current_player === 0 ? discard : undefined}
        server={server}
        gameId={gameId}
        playerIndex={0}
        activePlayer={state?.current_player}
      />
    </div>
    </>
  );
}
