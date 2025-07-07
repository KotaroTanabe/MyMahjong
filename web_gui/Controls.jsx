import React, { useState } from 'react';
import Button from './Button.jsx';

export default function Controls({
  server,
  gameId,
  playerIndex = 0,
  activePlayer = null,
  aiActive = false,
  allowedActions = [],
  log = () => {},
}) {
  const [message, setMessage] = useState('');


  async function simple(action, payload = {}) {
    try {
      log('debug', `POST /games/${gameId}/action ${action} - control button`);
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

  async function shanten() {
    try {
      log('debug', `GET /games/${gameId}/shanten/${playerIndex} - shanten button`);
      const resp = await fetch(
        `${server.replace(/\/$/, '')}/games/${gameId}/shanten/${playerIndex}`
      );
      if (resp.ok) {
        const data = await resp.json();
        setMessage(`Shanten: ${data.shanten}`);
      } else {
        setMessage(`Error ${resp.status}`);
      }
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

  const active = playerIndex === activePlayer && !aiActive;
  const isAllowed = (action) => active && allowedActions.includes(action);

  return (
    <div className="controls">
      <Button onClick={chi} disabled={!isAllowed('chi')}>Chi</Button>
      <Button onClick={pon} disabled={!isAllowed('pon')}>Pon</Button>
      <Button onClick={kan} disabled={!isAllowed('kan')}>Kan</Button>
      <Button onClick={riichi} disabled={!isAllowed('riichi')}>Riichi</Button>
      <Button onClick={tsumo} disabled={!isAllowed('tsumo')}>Tsumo</Button>
      <Button onClick={ron} disabled={!isAllowed('ron')}>Ron</Button>
      <Button onClick={skip} disabled={!isAllowed('skip')}>Skip</Button>
      <Button onClick={shanten}>Shanten</Button>
      {message && <div className="message">{message}</div>}
    </div>
  );
}
