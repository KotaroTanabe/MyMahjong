import React from 'react';

export default function River({ tiles = [] }) {
  return (
    <div className="river">
      {tiles.map((t, i) => (
        <span key={i} className="tile">{t}</span>
      ))}
    </div>
  );
}
