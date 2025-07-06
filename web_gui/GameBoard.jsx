import React, { useEffect, useRef, useState } from 'react';
import CenterDisplay from './CenterDisplay.jsx';
import PlayerPanel from './PlayerPanel.jsx';
import { tileToEmoji, sortTiles } from './tileUtils.js';
import ErrorModal from './ErrorModal.jsx';

function tileLabel(tile) {
  return tileToEmoji(tile);
}
export default function GameBoard({
  state,
  server,
  gameId,
  peek = false,
  sortHand = false,
}) {
  const players = state?.players ?? [];
  const south = players[0];
  const west = players[1];
  const north = players[2];
  const east = players[3];

  const prevPlayer = useRef(null);
  const [error, setError] = useState(null);
  // Players 1-3 (west, north, east) act as AI by default
  const [aiPlayers, setAiPlayers] = useState([false, true, true, true]);

  function toggleAI(idx) {
    setAiPlayers((a) => {
      const arr = a.slice();
      arr[idx] = !arr[idx];
      return arr;
    });
  }

  useEffect(() => {
    const current = state?.current_player;
    if (!gameId || current == null || current === prevPlayer.current) return;
    prevPlayer.current = current;
    const tiles = state?.players?.[current]?.hand?.tiles ?? [];
    if (tiles.length === 13) {
      const action = aiPlayers[current] ? 'auto' : 'draw';
      fetch(`${server.replace(/\/$/, '')}/games/${gameId}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_index: current, action }),
      }).catch(() => {});
    }
  }, [state?.current_player, gameId, server, state?.players, aiPlayers]);

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
  const southTiles = south?.hand?.tiles ?? null;
  const southHand = southTiles
    ? sortHand
      ? sortTiles(southTiles)
      : southTiles
    : defaultHand;

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
      const resp = await fetch(`${server.replace(/\/$/, '')}/games/${gameId}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_index: 0, action: 'discard', tile }),
      });
      if (!resp.ok) {
        setError(`Discard failed: ${resp.status}`);
      }
    } catch {
      setError('Failed to contact server');
    }
  }

  const boardClass = 'board-grid';

  return (
    <>
      <CenterDisplay
        remaining={remaining}
        dora={dora}
        honba={state?.honba ?? 0}
        riichiSticks={state?.riichi_sticks ?? 0}
      />
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
        aiActive={aiPlayers[2]}
        toggleAI={toggleAI}
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
        aiActive={aiPlayers[1]}
        toggleAI={toggleAI}
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
        aiActive={aiPlayers[3]}
        toggleAI={toggleAI}
      />
      <PlayerPanel
        seat="south"
        player={south}
        hand={southHand}
        melds={southMelds}
        riverTiles={(south?.river ?? []).map(tileLabel)}
        onDiscard={
          state?.current_player === 0 && !aiPlayers[0] ? discard : undefined
        }
        server={server}
        gameId={gameId}
        playerIndex={0}
        activePlayer={state?.current_player}
        aiActive={aiPlayers[0]}
        toggleAI={toggleAI}
      />
    </div>
    <ErrorModal message={error} onClose={() => setError(null)} />
    </>
  );
}
