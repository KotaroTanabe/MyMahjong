import { useEffect, useState } from 'react';
import Hand from './Hand.jsx';
import Button from './Button.jsx';
import { sortTiles } from './tileUtils.js';

export default function ShantenQuiz({ server, sortHand = true }) {
  const [hand, setHand] = useState(null);
  const [guess, setGuess] = useState('');
  const [answer, setAnswer] = useState(null);

  async function loadHand() {
    try {
      const resp = await fetch(`${server.replace(/\/$/, '')}/shanten-quiz`);
      if (resp.ok) {
        setHand(await resp.json());
        setGuess('');
        setAnswer(null);
      }
    } catch {
      setHand(null);
    }
  }

  async function check() {
    try {
      const resp = await fetch(
        `${server.replace(/\/$/, '')}/shanten-quiz/check`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ hand }),
        },
      );
      if (resp.ok) {
        const data = await resp.json();
        setAnswer(data.shanten);
      }
    } catch {
      // ignore
    }
  }

  useEffect(() => {
    loadHand();
  }, []);

  if (!hand) {
    return <div>Loading...</div>;
  }

  const tiles = sortHand ? sortTiles(hand) : hand;

  return (
    <div className="shanten-quiz">
      <Hand tiles={tiles} />
      <div className="field is-grouped is-align-items-flex-end">
        <label className="label mr-2">
          Shanten:
          <input
            className="input"
            type="number"
            value={guess}
            onChange={(e) => setGuess(e.target.value)}
            style={{ width: '4em' }}
          />
        </label>
        <div className="control">
          <Button onClick={check}>Check</Button>
        </div>
      </div>
      {answer !== null && (
        <div>{Number(guess) === answer ? 'Correct!' : `Shanten is ${answer}`}</div>
      )}
      <Button onClick={loadHand}>Next Hand</Button>
    </div>
  );
}
