import { useEffect, useState } from 'react';
import Hand from './Hand.jsx';
import Button from './Button.jsx';

export default function ShantenQuiz({ server }) {
  const [hand, setHand] = useState([]);
  const [guess, setGuess] = useState('');
  const [result, setResult] = useState(null);

  async function loadHand() {
    try {
      const resp = await fetch(`${server.replace(/\/$/, '')}/shanten-quiz`);
      if (resp.ok) {
        const data = await resp.json();
        setHand(data.hand);
        setGuess('');
        setResult(null);
      }
    } catch {
      setHand(null);
    }
  }

  async function submit() {
    try {
      const resp = await fetch(`${server.replace(/\/$/, '')}/shanten-quiz/check`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ hand, guess: Number(guess) }),
      });
      if (resp.ok) {
        setResult(await resp.json());
      }
    } catch {
      // ignore
    }
  }

  useEffect(() => {
    loadHand();
  }, []);


  return (
    <div className="shanten-quiz">
      <Hand tiles={hand} />
      <div className="field has-addons mt-2">
        <input
          aria-label="Shanten guess"
          className="input"
          type="number"
          value={guess}
          onChange={(e) => setGuess(e.target.value)}
          style={{ width: '5em' }}
        />
        <div className="control">
          <Button onClick={submit}>Submit</Button>
        </div>
      </div>
      {result && (
        <div>{result.correct ? 'Correct!' : `Shanten is ${result.actual}`}</div>
      )}
      <Button onClick={loadHand}>Next Hand</Button>
    </div>
  );
}
