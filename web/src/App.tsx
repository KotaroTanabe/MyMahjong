import { GameBoard } from './components/GameBoard.js';
import { useGame } from './hooks/useGame.js';

export default function App(): JSX.Element {
  const { hand, discards, wallCount, draw, discard, score } = useGame();
  return (
    <div className="app">
      <h1>My Mahjong</h1>
      <p>Wall tiles left: {wallCount}</p>
      <button onClick={draw} disabled={wallCount === 0}>Draw</button>
      {score.han > 0 && (
        <p className="score">{`${score.yaku.join(', ')}: ${score.points} points`}</p>
      )}
      <GameBoard currentHand={hand} currentDiscards={discards} onDiscard={discard} />
    </div>
  );
}
