import { useEffect, useState } from 'react';
import GameBoard from './GameBoard.jsx';
import './style.css';

export default function App() {
  const [server, setServer] = useState('http://localhost:8000');
  const [status, setStatus] = useState('Contacting server...');
  const [players, setPlayers] = useState('A,B,C,D');
  const [gameState, setGameState] = useState(null);

  async function fetchStatus() {
    setStatus('Contacting server...');
    try {
      const resp = await fetch(`${server.replace(/\/$/, '')}/health`);
      if (resp.ok) {
        const data = await resp.json();
        setStatus(`Server status: ${data.status} (${server})`);
      } else {
        setStatus(`Server error: ${resp.status} (${server})`);
      }
    } catch {
      setStatus(`Failed to contact server at ${server}`);
    }
  }

  async function startGame() {
    try {
      const resp = await fetch(`${server.replace(/\/$/, '')}/games`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ players: players.split(',').map((p) => p.trim()) }),
      });
      if (resp.ok) {
        const data = await resp.json();
        setGameState(data);
        setStatus('Game started');
      } else {
        setStatus(`Failed to start game (${resp.status})`);
      }
    } catch {
      setStatus(`Failed to contact server at ${server}`);
    }
  }

  useEffect(() => {
    fetchStatus();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <h1>MyMahjong GUI</h1>
      <div>
        <label>
          Server:
          <input
            value={server}
            onChange={(e) => setServer(e.target.value)}
            style={{ width: '20em' }}
          />
        </label>
        <button onClick={fetchStatus}>Retry</button>
      </div>
      <div>
        <label>
          Players:
          <input
            value={players}
            onChange={(e) => setPlayers(e.target.value)}
            style={{ width: '20em' }}
          />
        </label>
        <button onClick={startGame}>Start Game</button>
      </div>
      <GameBoard state={gameState} server={server} />
      <p>{status}</p>
    </>
  );
}
