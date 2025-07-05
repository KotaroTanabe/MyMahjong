import React from 'react';
import Hand from './Hand.jsx';
import River from './River.jsx';
import MeldArea from './MeldArea.jsx';
import CenterDisplay from './CenterDisplay.jsx';
import Controls from './Controls.jsx';

export default function GameBoard() {
  const hand = Array(13).fill('🀫');
  return (
    <div className="board-grid">
      <div className="north seat">
        <MeldArea melds={[]} />
        <River tiles={[]} />
        <Hand tiles={hand} />
      </div>
      <div className="west seat">
        <MeldArea melds={[]} />
        <River tiles={[]} />
        <Hand tiles={hand} />
      </div>
      <div className="center">
        <CenterDisplay />
      </div>
      <div className="east seat">
        <MeldArea melds={[]} />
        <River tiles={[]} />
        <Hand tiles={hand} />
      </div>
      <div className="south seat">
        <River tiles={[]} />
        <Hand tiles={hand} />
        <Controls />
        <MeldArea melds={[]} />
      </div>
    </div>
  );
}
