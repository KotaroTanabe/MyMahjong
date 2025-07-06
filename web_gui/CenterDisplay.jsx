import React from 'react';

export default function CenterDisplay({
  remaining = 0,
  dora = [],
  honba = 0,
  riichiSticks = 0,
}) {
  return (
    <div className="center-display">
      <div className="remaining">Remaining: {remaining}</div>
      <div className="dora">Dora: {dora.join(' ')}</div>
      <div className="counts">
        Honba: {honba} | Riichi: {riichiSticks}
      </div>
    </div>
  );
}
