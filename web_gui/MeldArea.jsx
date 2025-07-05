import React from 'react';

export default function MeldArea({ melds = [] }) {
  return (
    <div className="meld-area">
      {melds.map((meld, mIdx) => (
        <div key={mIdx} className="meld">
          {meld.map((t, i) => (
            typeof t === 'string' ? (
              <span key={i} className="tile">{t}</span>
            ) : (
              <span key={i} className="tile">
                <img src={t.src} alt={t.alt} />
              </span>
            )
          ))}
        </div>
      ))}
    </div>
  );
}

