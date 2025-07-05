import React, { useState } from 'react';
import Button from './Button.jsx';

export default function Controls({ server, gameId }) {
  const [message, setMessage] = useState('');


  async function simple(action, payload = {}) {
    try {
      await fetch(`${server.replace(/\/$/, '')}/games/${gameId}/action`, {
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
      <Button onClick={chi}>Chi</Button>
      <Button onClick={pon}>Pon</Button>
      <Button onClick={kan}>Kan</Button>
      <Button onClick={riichi}>Riichi</Button>
      <Button onClick={tsumo}>Tsumo</Button>
      <Button onClick={ron}>Ron</Button>
      <Button onClick={skip}>Skip</Button>
      {message && <div className="message">{message}</div>}
    </div>
  );
}
