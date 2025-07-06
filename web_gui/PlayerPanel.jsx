import React from 'react';
import Hand from './Hand.jsx';
import River from './River.jsx';
import MeldArea from './MeldArea.jsx';
import Controls from './Controls.jsx';

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
  actions = {},
}) {
  return (
    <div className={`${seat} seat player-panel`}>
      <div className="player-header">
        <span className="riichi-stick">{player?.riichi ? '|' : '\u00a0'}</span>
        <span>{(player ? player.name : seat) + (player ? ` ${player.score}` : '')}</span>
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
        {...actions}
      />
    </div>
  );
}
