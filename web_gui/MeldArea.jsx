import React from 'react';

export default function MeldArea({ melds = [] }) {
  return (
    <div className="meld-area">
      {melds.map((meld, mIdx) => (
        <div key={mIdx} className="meld">
          {meld.map((t, i) => (
            <span key={i} className="tile">{t}</span>
          ))}
        </div>
      ))}
    </div>
  );
}

