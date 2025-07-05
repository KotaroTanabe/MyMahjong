import { useEffect, useState } from 'react';
import GameBoard from './GameBoard.jsx';
import './style.css';

export default function App() {
  const [status, setStatus] = useState('Contacting server...');

  useEffect(() => {
    async function fetchStatus() {
      try {
        const resp = await fetch('http://localhost:8000/health');
        if (resp.ok) {
          const data = await resp.json();
          setStatus(`Server status: ${data.status}`);
        } else {
          setStatus(`Server error: ${resp.status}`);
        }
      } catch {
        setStatus('Failed to contact server');
      }
    }
    fetchStatus();
  }, []);

  return (
    <>
      <h1>MyMahjong GUI</h1>
      <GameBoard />
      <p>{status}</p>
    </>
  );
}
