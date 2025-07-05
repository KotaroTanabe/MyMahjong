import { useEffect, useState } from 'react';
import GameBoard from './GameBoard.jsx';
import './style.css';

export default function App() {
  const [server, setServer] = useState('http://localhost:8000');
  const [status, setStatus] = useState('Contacting server...');

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
      <GameBoard />
      <p>{status}</p>
    </>
  );
}
