import { useEffect, useRef, useState } from 'react';
import GameBoard from './GameBoard.jsx';
import Practice from './Practice.jsx';
import { applyEvent } from './applyEvent.js';
import Button from './Button.jsx';
import './style.css';
import { FiRefreshCw, FiEye, FiEyeOff, FiCheck } from "react-icons/fi";

export default function App() {
  const [server, setServer] = useState(
    () => localStorage.getItem('serverUrl') || 'http://localhost:8000',
  );
  const [status, setStatus] = useState('Contacting server...');
  const [connectionStatus, setConnectionStatus] = useState(null);
  const [players, setPlayers] = useState('A,B,C,D');
  const [gameId, setGameId] = useState(() => localStorage.getItem('gameId') || '');
  const [gameState, setGameState] = useState(null);
  const [events, setEvents] = useState([]);
  const [mode, setMode] = useState('game');
  const [peek, setPeek] = useState(false);
  const wsRef = useRef(null);

  useEffect(() => {
    localStorage.setItem('serverUrl', server);
  }, [server]);

  useEffect(() => {
    if (gameId) localStorage.setItem('gameId', gameId);
  }, [gameId]);

  async function fetchStatus() {
    setStatus('Contacting server...');
    setConnectionStatus(null);
    try {
      const resp = await fetch(`${server.replace(/\/$/, '')}/health`);
      if (resp.ok) {
        const data = await resp.json();
        setStatus(`Server status: ${data.status} (${server})`);
        setConnectionStatus('ok');
      } else {
        setStatus(`Server error: ${resp.status} (${server})`);
        setConnectionStatus(`Server error: ${resp.status}`);
      }
    } catch {
      setStatus(`Failed to contact server at ${server}`);
      setConnectionStatus('Failed to contact server');
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
        setGameId(String(data.id));
        localStorage.setItem('gameId', String(data.id));
        setStatus('Game started');
        openWebSocket(data.id);
      } else {
        setStatus(`Failed to start game (${resp.status})`);
      }
    } catch {
      setStatus(`Failed to contact server at ${server}`);
    }
  }

  async function fetchGameState(id = gameId) {
    try {
      if (!id) return;
      const resp = await fetch(`${server.replace(/\/$/, '')}/games/${id}`);
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

  function openWebSocket(id = gameId) {
    if (!id) return;
    const url = `${server.replace(/\/$/, '').replace('http', 'ws')}/ws/${id}`;
    const ws = new WebSocket(url);
    ws.onopen = () => setStatus('WebSocket connected');
    ws.onmessage = handleMessage;
    wsRef.current = ws;
  }

  useEffect(() => {
    fetchStatus();
    if (gameId) {
      fetchGameState(gameId);
      openWebSocket(gameId);
    }
    return () => {
      wsRef.current?.close();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <div className="field is-grouped is-align-items-flex-end">
        <label className="label mr-2">
          Server:
          <input
            className="input"
            value={server}
            onChange={(e) => setServer(e.target.value)}
            style={{ width: '20em' }}
          />
        </label>
        <div className="control">
          <Button aria-label="Retry" onClick={fetchStatus}><FiRefreshCw /></Button>
        </div>
        {connectionStatus === 'ok' ? (
          <span aria-label="Server ok" className="icon has-text-success ml-2">
            <FiCheck />
          </span>
        ) : connectionStatus ? (
          <span aria-label="Server error" className="ml-2 has-text-danger">
            {connectionStatus}
          </span>
        ) : null}
      </div>
      <div className="field">
        <label className="label">
          Mode:
          <span className="select ml-2">
            <select value={mode} onChange={(e) => setMode(e.target.value)}>
              <option value="game">Game</option>
              <option value="practice">Practice</option>
            </select>
          </span>
        </label>
      </div>
      <div className="field is-grouped is-align-items-flex-end">
        <label className="label mr-2">Peek:</label>
        <div className="control">
          <Button
            aria-label="Toggle peek"
            onClick={() => setPeek(!peek)}
          >
            {peek ? <FiEyeOff /> : <FiEye />}
          </Button>
        </div>
      </div>
      <div className="field is-grouped is-align-items-flex-end">
        <label className="label mr-2">
          Players:
          <input
            className="input"
            value={players}
            onChange={(e) => setPlayers(e.target.value)}
            style={{ width: '20em' }}
          />
        </label>
        <div className="control">
          <Button onClick={startGame}>Start Game</Button>
        </div>
      </div>
      <div className="field is-grouped is-align-items-flex-end">
        <label className="label mr-2">
          Game ID:
          <input
            className="input"
            value={gameId}
            onChange={(e) => setGameId(e.target.value)}
            style={{ width: '5em' }}
          />
        </label>
        <div className="control">
          <Button onClick={() => { fetchGameState(); openWebSocket(); }}>
            Join Game
          </Button>
        </div>
      </div>
      {mode === 'game' ? (
        <GameBoard
          state={gameState}
          server={server}
          gameId={gameId}
          peek={peek}
        />
      ) : (
        <Practice server={server} />
      )}
      {mode === 'game' && (
        <div className="event-log">
          <h2>Events</h2>
          <ul>
            {events.map((e, i) => (
              <li key={i}>{e}</li>
            ))}
          </ul>
        </div>
      )}
      <p>{status}</p>
    </>
  );
}
