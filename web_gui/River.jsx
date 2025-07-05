import React from 'react';

export default function River({ tiles = [] }) {
  return (
    <div className="river">
      {tiles.map((t, i) => (
        typeof t === 'string' ? (
          <span key={i} className="tile">{t}</span>
        ) : (
          <span key={i} className="tile">
            <img src={t.src} alt={t.alt} />
          </span>
        )
      ))}
    </div>
  );
}
