import React, { useEffect, useRef, useState } from 'react';
import { FaUser, FaRobot } from 'react-icons/fa';
import Hand from './Hand.jsx';
import River from './River.jsx';
import MeldArea from './MeldArea.jsx';
import Controls from './Controls.jsx';
import Button from './Button.jsx';
import { getAllowedActions } from './allowedActions.js';

export default function PlayerPanel({
  seat,
  player,
  hand,
  melds,
  riverTiles,
  onDiscard,
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
}) {
  const waiting = state?.waiting_for_claims ?? [];
  const active = playerIndex === activePlayer || waiting.includes(playerIndex);
  const [actions, setActions] = useState(allowedActions);
  const controllerRef = useRef(null);

  useEffect(() => {
    setActions(allowedActions);
  }, [allowedActions]);

  useEffect(() => {
    if (!server || !gameId) return;
    const controller = new AbortController();
    controllerRef.current?.abort();
    controllerRef.current = controller;
    getAllowedActions(server, gameId, playerIndex, log, { signal: controller.signal })
      .then((acts) => {
        if (Array.isArray(acts)) setActions(acts);
      })
      .catch(() => {});
    return () => controller.abort();
  }, [server, gameId, playerIndex]);
  return (
    <div className={`${seat} seat player-panel${active ? ' active-player' : ''}`}>
      <div className="player-header">
        <span className="riichi-stick">{player?.riichi ? '|' : '\u00a0'}</span>
        <span className="player-name">{(player ? player.name : seat) + (player ? ` ${player.score}` : '')}</span>
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
        aiActive={aiActive}
        allowedActions={actions}
        log={log}
      />
    </div>
  );
}
