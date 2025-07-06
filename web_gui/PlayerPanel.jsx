import React from 'react';
import { FiCpu } from 'react-icons/fi';
import Hand from './Hand.jsx';
import River from './River.jsx';
import MeldArea from './MeldArea.jsx';
import Controls from './Controls.jsx';
import Button from './Button.jsx';

export default function PlayerPanel({
  seat,
  player,
  hand,
  melds,
  riverTiles,
  onDiscard,
  server,
  gameId,
  playerIndex,
  activePlayer,
  aiActive = false,
  toggleAI,
}) {
  const active = playerIndex === activePlayer;
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
          <FiCpu />
        </Button>
      </div>
      <River tiles={riverTiles} />
      <div className="hand-with-melds">
        <Hand tiles={hand} onDiscard={onDiscard} />
        <MeldArea melds={melds} />
      </div>
      <Controls
        server={server}
        gameId={gameId}
        playerIndex={playerIndex}
        activePlayer={activePlayer}
        aiActive={aiActive}
      />
    </div>
  );
}
