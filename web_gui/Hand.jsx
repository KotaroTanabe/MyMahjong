import React from 'react';
import { tileToEmoji, tileDescription } from './tileUtils.js';

export default function Hand({ tiles = [], onDiscard }) {
  return (
    <div className="hand">
      {tiles.map((t, i) => {
        const label = typeof t === 'string' ? t : tileToEmoji(t);
        const alt = typeof t === 'string' ? t : tileDescription(t);
        return onDiscard ? (
          <button
            key={i}
            className="mj-tile"
            onClick={() => onDiscard(t)}
            aria-label={`Discard ${alt}`}
          >
            {label}
          </button>
        ) : (
          <span key={i} className="mj-tile">{label}</span>
        );
      })}
    </div>
  );
}
