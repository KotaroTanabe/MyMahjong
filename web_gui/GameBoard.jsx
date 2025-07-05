import React from 'react';

export default function GameBoard() {
  return (
    <div className="board-grid">
      <div className="north seat">North</div>
      <div className="west seat">West</div>
      <div className="center">Board</div>
      <div className="east seat">East</div>
      <div className="south seat">South</div>
    </div>
  );
}
