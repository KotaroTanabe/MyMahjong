import React, { useEffect, useRef } from 'react';
import CenterDisplay from './CenterDisplay.jsx';
import PlayerPanel from './PlayerPanel.jsx';
import { tileToEmoji } from './tileUtils.js';

function tileLabel(tile) {
  return tileToEmoji(tile);
}

function availableActions(state, idx) {
  const player = state?.players?.[idx];
  if (!state || !player) return {};
  const last = state.last_discard;
  const lastPlayer = state.last_discard_player;
  const counts = {};
  for (const t of player.hand?.tiles ?? []) {
    const key = `${t.suit}-${t.value}`;
    counts[key] = (counts[key] ?? 0) + 1;
  }
  const lastKey = last ? `${last.suit}-${last.value}` : null;
  const canChi =
    !!(
      last &&
      lastPlayer != null &&
      (lastPlayer + 1) % (state.players?.length ?? 4) === idx
    );
  const canPon = !!(last && lastPlayer !== idx && (counts[lastKey] ?? 0) >= 2);
  const canKan =
    (last && lastPlayer !== idx && (counts[lastKey] ?? 0) >= 3) ||
    Object.values(counts).some((c) => c >= 4);
  const isCurrent = state.current_player === idx;
  return { canChi, canPon, canKan, canRiichi: isCurrent, canTsumo: isCurrent, canRon: !!(last && lastPlayer !== idx), canSkip: isCurrent };
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

  const boardClass = 'board-grid';

  return (
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
        actions={availableActions(state, 2)}
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
        actions={availableActions(state, 3)}
      />
      <div className="center">
        <CenterDisplay remaining={remaining} dora={dora} />
      </div>
      <PlayerPanel
        seat="west"
        player={west}
        hand={westHand}
        melds={westMelds}
        riverTiles={(west?.river ?? []).map(tileLabel)}
        server={server}
        gameId={gameId}
        playerIndex={1}
        actions={availableActions(state, 1)}
      />
      <PlayerPanel
        seat="south"
        player={south}
        hand={southHand}
        melds={southMelds}
        riverTiles={(south?.river ?? []).map(tileLabel)}
        onDiscard={discard}
        server={server}
        gameId={gameId}
        playerIndex={0}
        actions={availableActions(state, 0)}
      />
    </div>
  );
}
