import React from 'react';

export default function CenterDisplay({ remaining = 0, dora = [] }) {
  return (
    <div className="center-display">
      <div className="remaining">Remaining: {remaining}</div>
      <div className="dora">
        Dora:{' '}
        {dora.map((t, i) => (
          typeof t === 'string' ? (
            <span key={i}>{t}</span>
          ) : (
            <img key={i} src={t.src} alt={t.alt} />
          )
        ))}
      </div>
    </div>
  );
}
