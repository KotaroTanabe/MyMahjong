import React, { useState } from 'react';
import Button from './Button.jsx';

export default function Controls({
  server,
  gameId,
  playerIndex = 0,
  activePlayer = null,
  aiActive = false,
}) {
  const [message, setMessage] = useState('');


  async function simple(action, payload = {}) {
    try {
      await fetch(`${server.replace(/\/$/, '')}/games/${gameId}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_index: playerIndex, action, ...payload }),
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

  const disabled = playerIndex !== activePlayer || aiActive;

  return (
    <div className="controls">
      <Button onClick={chi} disabled={disabled}>Chi</Button>
      <Button onClick={pon} disabled={disabled}>Pon</Button>
      <Button onClick={kan} disabled={disabled}>Kan</Button>
      <Button onClick={riichi} disabled={disabled}>Riichi</Button>
      <Button onClick={tsumo} disabled={disabled}>Tsumo</Button>
      <Button onClick={ron} disabled={disabled}>Ron</Button>
      <Button onClick={skip} disabled={disabled}>Skip</Button>
      {message && <div className="message">{message}</div>}
    </div>
  );
}
