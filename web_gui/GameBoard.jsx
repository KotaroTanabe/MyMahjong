import React, { useEffect, useRef, useState } from 'react';
import CenterDisplay from './CenterDisplay.jsx';
import PlayerPanel from './PlayerPanel.jsx';
import { tileToEmoji, sortTiles, sortTilesExceptLast } from './tileUtils.js';
import ErrorModal from './ErrorModal.jsx';
import ResultModal from './ResultModal.jsx';
import { getNextActions } from './nextActions.js';

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
  const prevWaiting = useRef([]);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  // Players 1-3 (west, north, east) act as AI by default
  const [aiPlayers, setAiPlayers] = useState([false, true, true, true]);
  const [aiTypes] = useState(['simple', 'simple', 'simple', 'simple']);

  function toggleAI(idx) {
    const enable = !aiPlayers[idx];
    setAiPlayers((a) => {
      const arr = a.slice();
      arr[idx] = enable;
      return arr;
    });
    if (
      enable &&
      idx === state?.current_player &&
      gameId &&
      state?.players?.[idx]?.hand?.tiles?.length >= 14
    ) {
      const tiles = state.players[idx].hand.tiles;
      const tile = tiles[tiles.length - 1];
      fetch(`${server.replace(/\/$/, '')}/games/${gameId}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          player_index: idx,
          action: 'discard',
          tile,
        }),
      }).catch(() => {});
    }
  }

  useEffect(() => {
    if (!gameId || result || state?.result) return;
    getNextActions(server, gameId).then((data) => {
      if (!data || !Array.isArray(data.actions)) return;
      const { player_index, actions } = data;
      if (actions.length === 1 && actions[0] === 'draw') {
        const ai = aiPlayers[player_index];
        const body = { player_index, action: ai ? 'auto' : 'draw' };
        if (ai) body.ai_type = aiTypes[player_index];
        fetch(`${server.replace(/\/$/, '')}/games/${gameId}/action`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        }).catch(() => {});
      }
    });
    const waiting = state?.waiting_for_claims ?? [];
    if (waiting.length > 0) {
      if (JSON.stringify(waiting) !== JSON.stringify(prevWaiting.current)) {
        prevWaiting.current = waiting.slice();
        waiting.forEach((idx) => {
          if (aiPlayers[idx]) {
            const body = {
              player_index: idx,
              action: 'auto',
              ai_type: aiTypes[idx],
            };
            fetch(`${server.replace(/\/$/, '')}/games/${gameId}/action`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(body),
            }).catch(() => {});
          }
        });
      }
      return;
    }
    prevWaiting.current = [];

    const current = state?.current_player;
    if (current == null || current === prevPlayer.current) return;
    prevPlayer.current = current;
    const tiles = state?.players?.[current]?.hand?.tiles ?? [];
    if (tiles.length === 13) {
      const action = aiPlayers[current] ? 'auto' : 'draw';
      const body = { player_index: current, action };
      if (action === 'auto') body.ai_type = aiTypes[current];
      fetch(`${server.replace(/\/$/, '')}/games/${gameId}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      }).catch(() => {});
    }
  }, [state?.current_player, state?.waiting_for_claims, gameId, server, state?.players, aiPlayers, aiTypes, result]);

  useEffect(() => {
    if (state?.result) {
      setResult(state.result);
    }
  }, [state?.result]);

  async function copyLog() {
    if (!gameId) return;
    try {
      const resp = await fetch(`${server.replace(/\/$/, '')}/games/${gameId}/log`);
      if (!resp.ok) return;
      const data = await resp.json();
      await navigator.clipboard.writeText(data.log);
    } catch {
      /* ignore */
    }
  }

  const defaultHand = Array(13).fill('🀫');

  function hasDrawnTile(player, index) {
    if (!player || state?.current_player !== index) return false;
    const count = player.hand?.tiles?.length ?? 0;
    return count % 3 === 2;
  }

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
      ? sortTilesExceptLast(southTiles)
      : southTiles
    : defaultHand;

  const northDrawn = hasDrawnTile(north, 2);
  const westDrawn = hasDrawnTile(west, 1);
  const eastDrawn = hasDrawnTile(east, 3);
  const southDrawn = hasDrawnTile(south, 0);

  const northMelds =
    north?.hand?.melds.map((m) => ({
      tiles: m.tiles.map(tileLabel),
      calledIndex: m.called_index ?? null,
    })) ?? [];
  const westMelds =
    west?.hand?.melds.map((m) => ({
      tiles: m.tiles.map(tileLabel),
      calledIndex: m.called_index ?? null,
    })) ?? [];
  const eastMelds =
    east?.hand?.melds.map((m) => ({
      tiles: m.tiles.map(tileLabel),
      calledIndex: m.called_index ?? null,
    })) ?? [];
  const southMelds =
    south?.hand?.melds.map((m) => ({
      tiles: m.tiles.map(tileLabel),
      calledIndex: m.called_index ?? null,
    })) ?? [];

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
        drawn={northDrawn}
        melds={northMelds}
        riverTiles={(north?.river ?? []).map(tileLabel)}
        state={state}
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
        drawn={westDrawn}
        melds={westMelds}
        riverTiles={(west?.river ?? []).map(tileLabel)}
        state={state}
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
        drawn={eastDrawn}
        melds={eastMelds}
        riverTiles={(east?.river ?? []).map(tileLabel)}
        state={state}
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
        drawn={southDrawn}
        melds={southMelds}
        riverTiles={(south?.river ?? []).map(tileLabel)}
        onDiscard={
          state?.current_player === 0 && !aiPlayers[0] ? discard : undefined
        }
        state={state}
        server={server}
        gameId={gameId}
        playerIndex={0}
        activePlayer={state?.current_player}
        aiActive={aiPlayers[0]}
        toggleAI={toggleAI}
      />
    </div>
    <ResultModal
      result={result}
      onClose={() => setResult(null)}
      onCopyLog={copyLog}
    />
    <ErrorModal message={error} onClose={() => setError(null)} />
    </>
  );
}
