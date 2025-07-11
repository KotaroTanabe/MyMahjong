import { useEffect, useState } from 'react';
import Hand from './Hand.jsx';
import Button from './Button.jsx';
import { tileToEmoji, tileDescription, sortTilesExceptLast } from './tileUtils.js';

export default function Practice({ server, sortHand = true, log = () => {} }) {
  const [problem, setProblem] = useState(null);
  const [suggestion, setSuggestion] = useState(null);
  const [chosen, setChosen] = useState(null);

  async function loadProblem() {
    try {
      log('debug', 'GET /practice - load new problem');
      const resp = await fetch(`${server.replace(/\/$/, '')}/practice`);
      if (resp.ok) {
        setProblem(await resp.json());
        setSuggestion(null);
        setChosen(null);
      }
    } catch {
      setProblem(null);
    }
  }

  async function choose(tile) {
    setChosen(tile);
    try {
      log('debug', 'POST /practice/suggest - request AI suggestion');
      const resp = await fetch(`${server.replace(/\/$/, '')}/practice/suggest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ hand: problem.hand }),
      });
      if (resp.ok) {
        setSuggestion(await resp.json());
      }
    } catch {
      // ignore
    }
  }

  useEffect(() => {
    loadProblem();
  }, []);

  if (!problem) {
    return <div>Loading...</div>;
  }

  const tiles = sortHand ? sortTilesExceptLast(problem.hand) : problem.hand;
  const drawn = problem.hand.length % 3 === 2;

  return (
    <div className="practice">
      <div>Seat wind: {problem.seat_wind}</div>
      <div> Dora indicator: {tileToEmoji(problem.dora_indicator)} </div>
      <Hand tiles={tiles} onDiscard={choose} drawn={drawn} />
      {chosen && (
        <div>You discarded {tileToEmoji(chosen)}</div>
      )}
      {suggestion && (
        <div>AI suggests discarding {tileToEmoji(suggestion)}</div>
      )}
      <Button onClick={loadProblem}>Next Problem</Button>
    </div>
  );
}
