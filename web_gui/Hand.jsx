import React from 'react';

export default function Hand({ tiles = [], onDiscard }) {
  return (
    <div className="hand">
      {tiles.map((t, i) => {
        const label = typeof t === 'string' ? t : `${t.suit[0]}${t.value}`;
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
