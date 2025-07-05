import { useEffect, useRef, useState } from 'react';
import GameBoard from './GameBoard.jsx';
import Practice from './Practice.jsx';
import { applyEvent } from './applyEvent.js';
import './style.css';

export default function App() {
  const [server, setServer] = useState('http://localhost:8000');
  const [status, setStatus] = useState('Contacting server...');
  const [players, setPlayers] = useState('A,B,C,D');
  const [gameId, setGameId] = useState(() => localStorage.getItem('gameId') || '');
  const [gameState, setGameState] = useState(null);
  const [events, setEvents] = useState([]);
  const [mode, setMode] = useState('game');
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

  function applyEvent(state, event) {
    if (!state) return state;
    const newState = JSON.parse(JSON.stringify(state));
    switch (event.name) {
      case 'start_game':
        return event.payload.state;
      case 'start_kyoku':
        return event.payload.state;
      case 'draw_tile': {
        const p = newState.players[event.payload.player_index];
        if (p) p.hand.tiles.push(event.payload.tile);
        if (newState.wall?.tiles?.length) newState.wall.tiles.pop();
        break;
      }
      case 'discard': {
        const p = newState.players[event.payload.player_index];
        if (p) {
          const { tile } = event.payload;
          const idx = p.hand.tiles.findIndex(
            (t) => t.suit === tile.suit && t.value === tile.value,
          );
          if (idx !== -1) p.hand.tiles.splice(idx, 1);
          p.river.push(tile);
        }
        break;
      }
      case 'meld': {
        const p = newState.players[event.payload.player_index];
        if (p) {
          event.payload.meld.tiles.forEach((m) => {
            const idx = p.hand.tiles.findIndex(
              (t) => t.suit === m.suit && t.value === m.value,
            );
            if (idx !== -1) p.hand.tiles.splice(idx, 1);
          });
          p.hand.melds.push(event.payload.meld);
        }
        break;
      }
      case 'riichi': {
        const p = newState.players[event.payload.player_index];
        if (p) p.riichi = true;
        break;
      }
      case 'tsumo':
      case 'ron': {
        newState.result = event.payload;
        break;
      }
      case 'skip': {
        const next = (event.payload.player_index + 1) % newState.players.length;
        newState.current_player = next;
        break;
      }
      default:
        break;
    }
    return newState;
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
          Mode:
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="game">Game</option>
            <option value="practice">Practice</option>
          </select>
        </label>
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
      <div>
        <label>
          Game ID:
          <input
            value={gameId}
            onChange={(e) => setGameId(e.target.value)}
            style={{ width: '5em' }}
          />
        </label>
        <button onClick={() => { fetchGameState(); openWebSocket(); }}>
          Join Game
        </button>
      </div>
      {mode === 'game' ? (
        <GameBoard state={gameState} server={server} gameId={gameId} />
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
