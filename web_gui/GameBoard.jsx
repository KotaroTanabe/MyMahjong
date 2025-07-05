import React from 'react';
import Hand from './Hand.jsx';
import River from './River.jsx';

export default function GameBoard() {
  const hand = Array(13).fill('🀫');
  return (
    <div className="board-grid">
      <div className="north seat">
        <River tiles={[]} />
        <Hand tiles={hand} />
      </div>
      <div className="west seat">
        <River tiles={[]} />
        <Hand tiles={hand} />
      </div>
      <div className="center">Board</div>
      <div className="east seat">
        <River tiles={[]} />
        <Hand tiles={hand} />
      </div>
      <div className="south seat">
        <River tiles={[]} />
        <Hand tiles={hand} />
      </div>
    </div>
  );
}
