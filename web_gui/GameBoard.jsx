import React, { useEffect, useRef, useState } from "react";
import CenterDisplay from "./CenterDisplay.jsx";
import PlayerPanel from "./PlayerPanel.jsx";
import { tileToEmoji, sortTiles, sortTilesExceptLast } from "./tileUtils.js";
import ErrorModal from "./ErrorModal.jsx";
import ResultModal from "./ResultModal.jsx";

function tileLabel(tile) {
  return tileToEmoji(tile);
}
export default function GameBoard({
  state,
  server,
  gameId,
  peek = false,
  sortHand = false,
  log = () => {},
  allowedActions = [[], [], [], []],
}) {
  const players = state?.players ?? [];
  const south = players[0];
  const west = players[1];
  const north = players[2];
  const east = players[3];

  const prevPlayer = useRef(null);
  const prevWaiting = useRef([]);
  const prevCounts = useRef([]);
  const lastDrawPlayer = useRef(null);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  // Players 1-3 (west, north, east) act as AI by default
  const [aiPlayers, setAiPlayers] = useState([false, true, true, true]);
  const [aiTypes] = useState(["simple", "simple", "simple", "simple"]);

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
      hasDrawnTile(state?.players?.[idx], idx)
    ) {
      const tiles = state.players[idx].hand.tiles;
      const tile = tiles[tiles.length - 1];
      log(
        "debug",
        `POST /games/${gameId}/action discard - enable AI autoplays`,
      );
      fetch(`${server.replace(/\/$/, "")}/games/${gameId}/action`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          player_index: idx,
          action: "discard",
          tile,
        }),
      }).catch(() => {});
    }
  }

  useEffect(() => {
    const counts = players.map((p) => p?.hand?.tiles?.length ?? 0);
    if (prevCounts.current.length) {
      counts.forEach((c, i) => {
        if (prevCounts.current[i] != null && c > prevCounts.current[i]) {
          lastDrawPlayer.current = i;
        }
      });
    }
    prevCounts.current = counts;
  }, [players]);

  useEffect(() => {
    if (!gameId || result || state?.result) return;
    const waiting = state?.waiting_for_claims ?? [];
    if (waiting.length > 0) {
      if (JSON.stringify(waiting) !== JSON.stringify(prevWaiting.current)) {
        prevWaiting.current = waiting.slice();
        waiting.forEach((idx) => {
          if (aiPlayers[idx]) {
            const body = {
              player_index: idx,
              action: "auto",
              ai_type: aiTypes[idx],
            };
            log("debug", `POST /games/${gameId}/action auto - resolve claims`);
            fetch(`${server.replace(/\/$/, "")}/games/${gameId}/action`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
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
    const tiles = state?.players?.[current]?.hand?.tiles ?? [];
    const last = state?.last_discard;
    const count = tiles.length;
    const drew = lastDrawPlayer.current === current;
    prevPlayer.current = current;
    if (count % 3 === 1 && last) {
      const action = aiPlayers[current] ? "auto" : "draw";
      const body = { player_index: current, action };
      if (action === "auto") body.ai_type = aiTypes[current];
      log(
        "debug",
        `POST /games/${gameId}/action ${action} - next player action`,
      );
      fetch(`${server.replace(/\/$/, "")}/games/${gameId}/action`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }).catch(() => {});
    } else if (count % 3 === 2 && aiPlayers[current] && drew) {
      const body = {
        player_index: current,
        action: "auto",
        ai_type: aiTypes[current],
      };
      log("debug", "POST /games/" + gameId + "/action auto - auto discard");
      fetch(`${server.replace(/\/$/, "")}/games/${gameId}/action`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }).catch(() => {});
      lastDrawPlayer.current = null;
    }
  }, [
    state?.current_player,
    state?.waiting_for_claims?.length ?? 0,
    gameId,
    server,
    aiPlayers,
    aiTypes,
    result,
  ]);


  useEffect(() => {
    if (state?.result) {
      setResult(state.result);
    }
  }, [state?.result]);

  async function copyLog() {
    if (!gameId) return;
    try {
      log("debug", `GET /games/${gameId}/log - user copied log`);
      const resp = await fetch(
        `${server.replace(/\/$/, "")}/games/${gameId}/log`,
      );
      if (!resp.ok) return;
      const data = await resp.json();
      await navigator.clipboard.writeText(data.log);
    } catch {
      /* ignore */
    }
  }

  const defaultHand = Array(13).fill("🀫");

  function hasDrawnTile(player, index) {
    if (!player || state?.current_player !== index) return false;
    const count = player.hand?.tiles?.length ?? 0;
    if (count % 3 !== 2) return false;
    return lastDrawPlayer.current === index;
  }

  function concealedHand(p) {
    const count = p?.hand?.tiles?.length ?? 13;
    return Array(count).fill("🀫");
  }

  const northHand = peek
    ? (north?.hand?.tiles.map(tileLabel) ?? defaultHand)
    : concealedHand(north);
  const westHand = peek
    ? (west?.hand?.tiles.map(tileLabel) ?? defaultHand)
    : concealedHand(west);
  const eastHand = peek
    ? (east?.hand?.tiles.map(tileLabel) ?? defaultHand)
    : concealedHand(east);
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
      calledFrom: m.called_from ?? null,
    })) ?? [];
  const westMelds =
    west?.hand?.melds.map((m) => ({
      tiles: m.tiles.map(tileLabel),
      calledIndex: m.called_index ?? null,
      calledFrom: m.called_from ?? null,
    })) ?? [];
  const eastMelds =
    east?.hand?.melds.map((m) => ({
      tiles: m.tiles.map(tileLabel),
      calledIndex: m.called_index ?? null,
      calledFrom: m.called_from ?? null,
    })) ?? [];
  const southMelds =
    south?.hand?.melds.map((m) => ({
      tiles: m.tiles.map(tileLabel),
      calledIndex: m.called_index ?? null,
      calledFrom: m.called_from ?? null,
    })) ?? [];

  const remaining = state?.wall?.tiles?.length ?? 0;
  const dora = state?.wall?.tiles?.[0] ? [tileLabel(state.wall.tiles[0])] : [];

  async function discard(tile) {
    try {
      if (!gameId) return;
      if (typeof tile === "string") return;
      log("debug", `POST /games/${gameId}/action discard - user clicked tile`);
      const resp = await fetch(
        `${server.replace(/\/$/, "")}/games/${gameId}/action`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ player_index: 0, action: "discard", tile }),
        },
      );
      if (!resp.ok) {
        let message = `Discard failed: ${resp.status}`;
        try {
          const data = await resp.json();
          if (data.detail) message = data.detail;
        } catch {}
        setError(message);
      }
    } catch {
      setError("Failed to contact server");
    }
  }

  const boardClass = "board-grid";

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
          allowedActions={allowedActions[2] || []}
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
          allowedActions={allowedActions[1] || []}
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
          allowedActions={allowedActions[3] || []}
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
          allowedActions={allowedActions[0] || []}
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
