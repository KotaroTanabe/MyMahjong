import React from 'react';
import { tileToEmoji } from './tileUtils.js';

export default function Hand({ tiles = [], onDiscard }) {
  return (
    <div className="hand">
      {tiles.map((t, i) => {
        const label = typeof t === 'string' ? t : tileToEmoji(t);
        return onDiscard ? (
          <button
            key={i}
            className="tile"
            onClick={() => onDiscard(t)}
          >
            {label}
          </button>
        ) : (
          <span key={i} className="tile">{label}</span>
        );
      })}
    </div>
  );
}
