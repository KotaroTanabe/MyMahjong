import React, { useState } from 'react';

export default function Controls({ server }) {
  const [message, setMessage] = useState('');

  async function draw() {
    try {
      const resp = await fetch(`${server.replace(/\/$/, '')}/games/1/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_index: 0, action: 'draw' }),
      });
      if (resp.ok) {
        const tile = await resp.json();
        setMessage(`Drew ${tile.suit} ${tile.value}`);
      } else {
        let data = null;
        try {
          data = await resp.json();
        } catch {
          // ignore
        }
        setMessage(data?.detail || 'Error drawing tile');
      }
    } catch {
      setMessage('Server unreachable');
    }
  }

  return (
    <div className="controls">
      <button onClick={draw}>Draw</button>
      {message && <div className="message">{message}</div>}
    </div>
  );
}
