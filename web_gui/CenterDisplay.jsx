import React from 'react';

export default function CenterDisplay({ remaining = 0, dora = [] }) {
  return (
    <div className="center-display">
      <div className="remaining">Remaining: {remaining}</div>
      <div className="dora">Dora: {dora.join(' ')}</div>
    </div>
  );
}
