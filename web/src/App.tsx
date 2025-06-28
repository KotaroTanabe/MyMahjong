import React from 'react';
import { Hand } from './components/Hand.js';
import { useGame } from './hooks/useGame.js';

export default function App(): JSX.Element {
  const { hand, discards, wallCount, draw, discard } = useGame();
  return (
    <div className="app">
      <h1>My Mahjong</h1>
      <p>Wall tiles left: {wallCount}</p>
      <button onClick={draw} disabled={wallCount === 0}>Draw</button>
      <h2>Your Hand</h2>
      <Hand tiles={hand} onDiscard={discard} />
      <h2>Discards</h2>
      <ul className="discards">
        {discards.map((t, i) => <li key={i}>{t.toString()}</li>)}
      </ul>
    </div>
  );
}
