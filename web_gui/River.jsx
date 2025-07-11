import React from 'react';

export default function River({
  tiles = [],
  style = {},
  highlightIndex = -1,
}) {
  const cells = Array.from({ length: 24 }, (_, i) => tiles[i] || null);
  return (
    <div className="river" style={style}>
      {cells.map((t, i) => (
        <span
          key={i}
          className={`mj-tile${i === highlightIndex ? ' waiting-discard' : ''}`}
        >
          {t ?? '\u00a0'}
        </span>
      ))}
    </div>
  );
}
