import React from 'react';

export default function Hand({ tiles = [] }) {
  return (
    <div className="hand">
      {tiles.map((t, i) => (
        <span key={i} className="tile">{t}</span>
      ))}
    </div>
  );
}
