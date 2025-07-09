import React from 'react';

export default function CenterDisplay({
  remaining = 0,
  dora = [],
  honba = 0,
  riichiSticks = 0,
  round = 1,
}) {
  const winds = ['\u6771', '\u5357', '\u897f', '\u5317'];
  const wind = winds[Math.floor((round - 1) / 4)] || winds[0];
  const hand = ((round - 1) % 4) + 1;
  const roundLabel = `${wind}${hand}\u5c40`;
  return (
    <div className="center-display">
      <div className="remaining">Remaining: {remaining}</div>
      <div className="dora">Dora: {dora.join(' ')}</div>
      <div className="counts">
        {roundLabel} | Honba: {honba} | Riichi: {riichiSticks}
      </div>
    </div>
  );
}
