import React from 'react';

export default function River({ tiles = [] }) {
  const cells = Array.from({ length: 24 }, (_, i) => tiles[i] || null);
  return (
    <div className="river">
      {cells.map((t, i) => (
        <span key={i} className="tile">
          {t ?? '\u00a0'}
        </span>
      ))}
    </div>
  );
}
