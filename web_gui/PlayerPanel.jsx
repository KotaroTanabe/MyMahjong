import React, { useEffect, useRef, useState, useMemo } from 'react';
import { FaUser, FaRobot } from 'react-icons/fa';
import Hand from './Hand.jsx';
import River from './River.jsx';
import MeldArea from './MeldArea.jsx';
import Controls from './Controls.jsx';
import Button from './Button.jsx';
import { getAllowedActions } from './allowedActions.js';
import ErrorModal from './ErrorModal.jsx';

const windChars = {
  east: '\u6771',
  south: '\u5357',
  west: '\u897f',
  north: '\u5317',
};

export default function PlayerPanel({
  seat,
  player,
  hand,
  melds,
  riverTiles,
  onDiscard,
  onRiichi,
  drawn = false,
  server,
  gameId,
  playerIndex,
  activePlayer,
  aiActive = false,
  toggleAI,
  state,
  log = () => {},
  allowedActions = [],
  selectingRiichi = false,
}) {
  const waiting = state?.waiting_for_claims ?? [];
  const isWaiting = waiting.includes(playerIndex);
  const active = playerIndex === activePlayer;
  const allowedActionsMemo = useMemo(
    () => allowedActions,
    [allowedActions.join(',')]
  );
  const [actions, setActions] = useState(allowedActionsMemo);
  const [waitingForRiichi, setWaitingForRiichi] = useState(false);
  const [error, setError] = useState(null);
  const controllerRef = useRef(null);
  const highlightIndex =
    (waiting.length > 0 && playerIndex === state?.last_discard_player)
      ? (player?.river?.length ?? 0) - 1
      : null;

  useEffect(() => {
    setActions(allowedActionsMemo);
    if (
      playerIndex === 0 &&
      allowedActionsMemo.length === 2 &&
      allowedActionsMemo.includes('riichi') &&
      allowedActionsMemo.includes('skip')
    ) {
      setWaitingForRiichi(true);
    } else if (playerIndex === 0) {
      setWaitingForRiichi(false);
    }
  }, [allowedActionsMemo]);

  useEffect(() => {
    if (!server || !gameId || !state) return;
    controllerRef.current?.abort();
    if (aiActive) {
      controllerRef.current = null;
      return;
    }
    const controller = new AbortController();
    controllerRef.current = controller;
    getAllowedActions(server, gameId, playerIndex, log, {
      signal: controller.signal,
      requestId: `panel-${playerIndex}`,
    })
      .then((acts) => {
        if (acts && acts.error) {
          setError(`Failed to fetch actions: ${acts.error}`);
        } else if (Array.isArray(acts)) {
          setActions(acts);
          if (
            playerIndex === 0 &&
            acts.length === 2 &&
            acts.includes('riichi') &&
            acts.includes('skip')
          ) {
            setWaitingForRiichi(true);
          } else if (playerIndex === 0) {
            setWaitingForRiichi(false);
          }
        }
      })
      .catch((err) => {
        if (err.name !== 'AbortError') {
          setError(`Failed to fetch actions: ${err.message}`);
        }
      });
    return () => controller.abort();
  }, [server, gameId, playerIndex, aiActive]);
  return (
    <div className={`${seat} seat player-panel${active ? ' active-player' : ''}`}>
      <div className="player-header">
        <span className="riichi-stick">{player?.riichi ? '|' : '\u00a0'}</span>
        <span className="player-name">
          {(player ? player.name : seat)}
          {player?.seat_wind ? ` (${windChars[player.seat_wind]})` : ''}
          {player ? ` ${player.score}` : ''}
        </span>
        <Button
          aria-label={aiActive ? 'Disable AI' : 'Enable AI'}
          className={`ai-btn${aiActive ? ' active' : ''}`}
          onClick={() => toggleAI?.(playerIndex)}
        >
          {aiActive ? <FaRobot /> : <FaUser />}
        </Button>
      </div>
      <River
        tiles={riverTiles}
        highlightIndex={highlightIndex}
        style={{ marginBottom: 'calc(var(--tile-font-size) * 0.8)' }}
      />
      <div className="hand-with-melds" style={{ position: 'relative', zIndex: 1 }}>
        <Hand tiles={hand} onDiscard={onDiscard} drawn={drawn} />
        <MeldArea melds={melds} />
      </div>
      <Controls
        server={server}
        gameId={gameId}
        playerIndex={playerIndex}
        activePlayer={activePlayer}
        waitingForClaims={waiting}
        waitingForRiichi={playerIndex === 0 ? waitingForRiichi : false}
        aiActive={aiActive}
        allowedActions={actions}
        lastDiscard={state?.last_discard}
        log={log}
        onError={setError}
        onRiichi={onRiichi}
        selectingRiichi={selectingRiichi}
      />
      {error && (
        <ErrorModal message={error} onClose={() => setError(null)} />
      )}
    </div>
  );
}
