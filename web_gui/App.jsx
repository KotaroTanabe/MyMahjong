import { useEffect, useRef, useState } from 'react';
import GameBoard from './GameBoard.jsx';
import { applyEvent } from './applyEvent.js';
import './style.css';

export default function App() {
  const [server, setServer] = useState('http://localhost:8000');
  const [status, setStatus] = useState('Contacting server...');
  const [players, setPlayers] = useState('A,B,C,D');
  const [gameState, setGameState] = useState(null);
  const [events, setEvents] = useState([]);
  const wsRef = useRef(null);

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
        openWebSocket();
      } else {
        setStatus(`Failed to start game (${resp.status})`);
      }
    } catch {
      setStatus(`Failed to contact server at ${server}`);
    }
  }

  async function fetchGameState() {
    try {
      const resp = await fetch(`${server.replace(/\/$/, '')}/games/1`);
      if (resp.ok) {
        setGameState(await resp.json());
      }
    } catch {
      // ignore
    }
  }


  function handleMessage(e) {
    try {
      const evt = JSON.parse(e.data);
      setEvents((evts) => [...evts.slice(-9), evt.name]);
      setGameState((s) => applyEvent(s, evt));
    } catch {
      // ignore parse errors
    }
  }

  function openWebSocket() {
    const url = `${server.replace(/\/$/, '').replace('http', 'ws')}/ws/1`;
    const ws = new WebSocket(url);
    ws.onopen = () => setStatus('WebSocket connected');
    ws.onmessage = handleMessage;
    wsRef.current = ws;
  }

  useEffect(() => {
    fetchStatus();
    return () => {
      wsRef.current?.close();
    };
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
      <div className="event-log">
        <h2>Events</h2>
        <ul>
          {events.map((e, i) => (
            <li key={i}>{e}</li>
          ))}
        </ul>
      </div>
      <p>{status}</p>
    </>
  );
}
