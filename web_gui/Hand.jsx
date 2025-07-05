import React from 'react';
import { tileToImage, tileDescription } from './tileUtils.js';

export default function Hand({ tiles = [], onDiscard }) {
  return (
    <div className="hand">
      {tiles.map((t, i) => {
        if (typeof t === 'string') {
          return (
            <span key={i} className="tile">{t}</span>
          );
        }
        const src = t.src || tileToImage(t);
        const alt = t.alt || tileDescription(t);
        return onDiscard ? (
          <button
            key={i}
            className="tile"
            onClick={() => onDiscard(t)}
            aria-label={`Discard ${alt}`}
          >
            <img src={src} alt={alt} />
          </button>
        ) : (
          <span key={i} className="tile">
            <img src={src} alt={alt} />
          </span>
        );
      })}
    </div>
  );
}
