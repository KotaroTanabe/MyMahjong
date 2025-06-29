import { GameBoard } from './components/GameBoard.js';
import { ScoreBoard } from './components/ScoreBoard.js';
import { useGame } from './hooks/useGame.js';

export default function App(): JSX.Element {
  const { hand, playerDiscards, melds, wallCount, doraIndicators,　draw, discard, pon, chi, kan, ron, score, scoreboard } = useGame();
  return (
    <div className="app">
      <h1>My Mahjong</h1>
      <button onClick={draw} disabled={wallCount === 0} aria-label="Draw">🀄</button>
      {score.han > 0 && (
        <p className="score">{`${score.yaku.join(', ')}: ${score.points} points`}</p>
      )}
      <ScoreBoard scores={scoreboard} />
      <GameBoard
        currentHand={hand}
        playerDiscards={playerDiscards}
        centerTiles={doraIndicators}
        wallCount={wallCount}
        currentMelds={melds}
        onDiscard={discard}
        onPon={pon}
        onChi={chi}
        onKan={kan}
        onRon={ron}
      />
    </div>
  );
}
