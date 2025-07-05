import { useEffect, useState } from 'react';
import Hand from './Hand.jsx';
import Button from './Button.jsx';
import { tileToImage, tileDescription } from './tileUtils.js';

export default function Practice({ server }) {
  const [problem, setProblem] = useState(null);
  const [suggestion, setSuggestion] = useState(null);
  const [chosen, setChosen] = useState(null);

  async function loadProblem() {
    try {
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

  return (
    <div className="practice">
      <div>Seat wind: {problem.seat_wind}</div>
      <div>
        Dora indicator:{' '}
        <img
          src={tileToImage(problem.dora_indicator)}
          alt={tileDescription(problem.dora_indicator)}
        />
      </div>
      <Hand tiles={problem.hand} onDiscard={choose} />
      {chosen && (
        <div>
          You discarded{' '}
          <img src={tileToImage(chosen)} alt={tileDescription(chosen)} />
        </div>
      )}
      {suggestion && (
        <div>
          AI suggests discarding{' '}
          <img src={tileToImage(suggestion)} alt={tileDescription(suggestion)} />
        </div>
      )}
      <Button onClick={loadProblem}>Next Problem</Button>
    </div>
  );
}
