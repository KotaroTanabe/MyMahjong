import React from 'react';

export default function MeldArea({ melds = [] }) {
  return (
    <div className="meld-area">
      {melds.map((meld, mIdx) => {
        const orientClass =
          meld.calledFrom === 1
            ? ' called-from-left'
            : meld.calledFrom === 2
            ? ' called-from-opposite'
            : meld.calledFrom === 3
            ? ' called-from-right'
            : '';
        return (
          <div key={mIdx} className="meld">
            {meld.tiles.map((t, i) => (
              <span
                key={i}
                className={`mj-tile${meld.calledIndex === i ? ' called-tile' : ''}${
                  meld.calledIndex === i ? orientClass : ''
                }`}
              >
                {t}
              </span>
            ))}
          </div>
        );
      })}
    </div>
  );
}

