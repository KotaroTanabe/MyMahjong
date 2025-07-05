import React from 'react';

export default function CenterDisplay({ remaining = 70, dora = ['\uD83C\uDE00'] }) {
  return (
    <div className="center-display">
      <div className="remaining">Remaining: {remaining}</div>
      <div className="dora">Dora: {dora.join(' ')}</div>
    </div>
  );
}
