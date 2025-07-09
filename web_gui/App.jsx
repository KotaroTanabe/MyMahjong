import { useEffect, useRef, useState } from 'react';
import GameBoard from './GameBoard.jsx';
import Practice from './Practice.jsx';
import ShantenQuiz from './ShantenQuiz.jsx';
import { applyEvent } from './applyEvent.js';
import Button from './Button.jsx';
import EventLogModal from './EventLogModal.jsx';
import { formatEvent, eventToMjaiJson } from './eventLog.js';
import { logNextActions } from './eventFlow.js';
import './style.css';
import { FiRefreshCw, FiEye, FiEyeOff, FiCheck, FiShuffle, FiSettings, FiCopy } from "react-icons/fi";

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
  const [allowedActions, setAllowedActions] = useState([[], [], [], []]);
  function log(level, message) {
    setEvents((evts) => [...evts.slice(-19), `[${level}] ${message}`]);
  }
  const [mode, setMode] = useState('game');
  const [peek, setPeek] = useState(false);
  const [sortHand, setSortHand] = useState(true);
  const [showSettings, setShowSettings] = useState(false);
  const [showLog, setShowLog] = useState(false);
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
      log('debug', 'POST /games - user started a new game');
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
      log('debug', `GET /games/${id} - restoring game state`);
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
      log('info', formatEvent(evt));
      if (evt.name === 'allowed_actions') {
        setAllowedActions(evt.payload?.actions || [[], [], [], []]);
        setEvents((evts) => {
          const line = `${formatEvent(evt)} ${eventToMjaiJson(evt)}`;
          return [...evts.slice(-9), line];
        });
        return;
      }
      setGameState((prev) => {
        const next = applyEvent(prev, evt);
        setEvents((evts) => {
          const lines = [];
          if (evt.name === 'draw_tile') {
            lines.push(formatEvent({ name: 'turn_start', payload: { player_index: evt.payload.player_index } }));
            lines.push(formatEvent(evt));
          } else if (evt.name === 'discard' || evt.name === 'meld' || evt.name === 'riichi' || evt.name === 'ron' || evt.name === 'tsumo' || evt.name === 'ryukyoku' || evt.name === 'start_kyoku' || evt.name === 'start_game' || evt.name === 'end_game' || evt.name === 'next_actions' || evt.name === 'skip') {
            lines.push(formatEvent(evt));
          } else {
            lines.push(formatEvent(evt));
          }
          const json = eventToMjaiJson(evt);
          const withJson = lines.map((l) => `${l} ${json}`);
          return [...evts.slice(-10 + withJson.length), ...withJson];
        });
        return next;
      });
      if (evt.name !== 'next_actions' && gameId) {
        logNextActions(server, gameId, log, (line) =>
          setEvents((evts) => [...evts.slice(-9), line]),
        );
      }
    } catch {
      // ignore parse errors
    }
  }

  async function copyEvents() {
    try {
      await navigator.clipboard.writeText(events.join('\n'));
    } catch {
      /* ignore */
    }
  }

  async function openLogModal() {
    if (!gameId) return;
    try {
      const resp = await fetch(`${server.replace(/\/$/, '')}/games/${gameId}/events`);
      if (resp.ok) {
        const data = await resp.json();
        const lines = data.events.map((evt) => {
          const text = formatEvent(evt);
          const json = eventToMjaiJson(evt);
          return `${text} ${json}`;
        });
        setEvents(lines);
      }
    } catch {
      /* ignore */
    }
    setShowLog(true);
  }

  async function downloadLog(url, filename) {
    try {
      const resp = await fetch(url);
      if (!resp.ok) return;
      const data = await resp.json();
      const blob = new Blob([data.log], { type: 'application/json' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      try {
        link.click();
      } catch {
        /* ignore */
      }
      URL.revokeObjectURL(link.href);
    } catch {
      /* ignore */
    }
  }

  async function downloadTenhou() {
    if (!gameId) return;
    await downloadLog(
      `${server.replace(/\/$/, '')}/games/${gameId}/log`,
      `game_${gameId}_tenhou.json`,
    );
  }

  async function downloadMjai() {
    if (!gameId) return;
    await downloadLog(
      `${server.replace(/\/$/, '')}/games/${gameId}/mjai-log`,
      `game_${gameId}_mjai.json`,
    );
  }

  function openWebSocket(id = gameId) {
    if (!id) return;
    const url = `${server.replace(/\/$/, '').replace('http', 'ws')}/ws/${id}`;
    const ws = new WebSocket(url);
    ws.onopen = () => setStatus('WebSocket connected');
    ws.onmessage = handleMessage;
    wsRef.current = ws;
  }

  function HeaderBar() {
    return (
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
          <Button aria-label="Retry" onClick={fetchStatus}>
            <FiRefreshCw />
          </Button>
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
        <label className="label ml-4">
          Mode:
          <span className="select ml-2">
            <select value={mode} onChange={(e) => setMode(e.target.value)}>
              <option value="game">Game</option>
              <option value="practice">Practice</option>
              <option value="shanten">Shanten Quiz</option>
            </select>
          </span>
        </label>
        {mode === 'game' && gameState && (
          <>
            <div className="control ml-2">
              <Button aria-label="Options" onClick={() => setShowSettings(true)}>
                <FiSettings />
              </Button>
            </div>
            <div className="control ml-2">
              <Button aria-label="Show log" onClick={openLogModal}>
                Log
              </Button>
            </div>
            <div className="control ml-2">
              <Button aria-label="Download MJAI log" onClick={downloadMjai}>
                MJAI
              </Button>
            </div>
            <div className="control ml-2">
              <Button aria-label="Download Tenhou log" onClick={downloadTenhou}>
                Tenhou
              </Button>
            </div>
          </>
        )}
        {mode === 'game' && (
          <>
            <div className="control ml-2">
            <Button
              aria-label="Toggle peek"
              title="Peek at opponents' hands"
              aria-pressed={peek}
              className={peek ? 'active' : ''}
              onClick={() => setPeek(!peek)}
            >
              {peek ? <FiEyeOff /> : <FiEye />}
            </Button>
            </div>
            <div className="control ml-2">
            <Button
              aria-label="Toggle sort"
              title="Sort hand"
              aria-pressed={sortHand}
              className={sortHand ? 'active' : ''}
              onClick={() => setSortHand(!sortHand)}
            >
              {sortHand ? <FiCheck /> : <FiShuffle />}
            </Button>
            </div>
          </>
        )}
      </div>
    );
  }

  function SetupFields() {
    return (
      <>
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
            <Button
              onClick={() => {
                fetchGameState();
                openWebSocket();
              }}
            >
              Join Game
            </Button>
          </div>
        </div>
      </>
    );
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
      <HeaderBar />
      {mode === 'game' && !gameState && <SetupFields />}
      {mode === 'game' && gameState && showSettings && (
        <div className="modal is-active">
          <div className="modal-background" onClick={() => setShowSettings(false)}></div>
          <div className="modal-content">
            <div className="box">
              <SetupFields />
            </div>
          </div>
          <button
            className="modal-close is-large"
            aria-label="close"
            onClick={() => setShowSettings(false)}
          ></button>
        </div>
      )}
      {mode === 'game' ? (
        <GameBoard
          state={gameState}
          server={server}
          gameId={gameId}
          peek={peek}
          sortHand={sortHand}
          log={log}
          allowedActions={allowedActions}
        />
      ) : mode === 'practice' ? (
        <Practice server={server} sortHand={sortHand} log={log} />
      ) : (
        <ShantenQuiz server={server} sortHand={sortHand} log={log} />
      )}
      {mode === 'game' && showLog && (
        <EventLogModal events={events} onClose={() => setShowLog(false)} onCopy={copyEvents} />
      )}
      <p>{status}</p>
    </>
  );
}
