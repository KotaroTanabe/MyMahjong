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

  async function simple(action, payload = {}) {
    try {
      await fetch(`${server.replace(/\/$/, '')}/games/1/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_index: 0, action, ...payload }),
      });
      setMessage(action);
    } catch {
      setMessage('Server unreachable');
    }
  }

  function chi() {
    simple('chi', { tiles: [{ suit: 'man', value: 1 }, { suit: 'man', value: 2 }, { suit: 'man', value: 3 }] });
  }

  function pon() {
    simple('pon', { tiles: [{ suit: 'pin', value: 1 }, { suit: 'pin', value: 1 }, { suit: 'pin', value: 1 }] });
  }

  function kan() {
    simple('kan', { tiles: [{ suit: 'sou', value: 2 }, { suit: 'sou', value: 2 }, { suit: 'sou', value: 2 }, { suit: 'sou', value: 2 }] });
  }

  function riichi() {
    simple('riichi');
  }

  function tsumo() {
    simple('tsumo', { tile: { suit: 'man', value: 1 } });
  }

  function ron() {
    simple('ron', { tile: { suit: 'man', value: 1 } });
  }

  function skip() {
    simple('skip');
  }

  return (
    <div className="controls">
      <button onClick={draw}>Draw</button>
      <button onClick={chi}>Chi</button>
      <button onClick={pon}>Pon</button>
      <button onClick={kan}>Kan</button>
      <button onClick={riichi}>Riichi</button>
      <button onClick={tsumo}>Tsumo</button>
      <button onClick={ron}>Ron</button>
      <button onClick={skip}>Skip</button>
      {message && <div className="message">{message}</div>}
    </div>
  );
}
