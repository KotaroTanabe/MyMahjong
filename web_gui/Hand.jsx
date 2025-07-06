import React from 'react';
import { tileToEmoji, tileDescription } from './tileUtils.js';

export default function Hand({ tiles = [], onDiscard }) {
  return (
    <div className="hand">
      {tiles.map((t, i) => {
        const label = typeof t === 'string' ? t : tileToEmoji(t);
        const alt = typeof t === 'string' ? t : tileDescription(t);
        const cls = `mj-tile${i === tiles.length - 1 ? ' drawn-tile' : ''}`;
        return onDiscard ? (
          <button
            key={i}
            className={cls}
            onClick={() => onDiscard(t)}
            aria-label={`Discard ${alt}`}
          >
            {label}
          </button>
        ) : (
          <span key={i} className={cls}>{label}</span>
        );
      })}
    </div>
  );
}
