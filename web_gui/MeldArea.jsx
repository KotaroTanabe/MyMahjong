import React from 'react';

export default function MeldArea({ melds = [] }) {
  return (
    <div className="meld-area">
      {melds.map((meld, mIdx) => (
        <div key={mIdx} className="meld">
          {meld.tiles.map((t, i) => (
            <span
              key={i}
              className={`mj-tile${meld.calledIndex === i ? ' called-tile' : ''}`}
            >
              {t}
            </span>
          ))}
        </div>
      ))}
    </div>
  );
}

