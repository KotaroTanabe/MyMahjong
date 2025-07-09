import React, { useState } from 'react';
import Button from './Button.jsx';
import ChiModal from './ChiModal.jsx';
import { getChiOptions } from './chiOptions.js';

export function Controls({
  server,
  gameId,
  playerIndex = 0,
  activePlayer = null,
  aiActive = false,
  allowedActions = [],
  waitingForClaims = [],
  lastDiscard = null,
  log = () => {},
  onError = () => {},
}) {
  const [message, setMessage] = useState('');
  const [chiOptions, setChiOptions] = useState(null);


  async function simple(action, payload = {}) {
    try {
      log('debug', `POST /games/${gameId}/action ${action} - control button`);
      const resp = await fetch(`${server.replace(/\/$/, '')}/games/${gameId}/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_index: playerIndex, action, ...payload }),
      });
      if (!resp.ok) {
        let msg = `Action ${action} failed: ${resp.status}`;
        try {
          const data = await resp.json();
          if (data.detail) msg = data.detail;
        } catch {}
        onError(msg);
      } else {
        setMessage(action);
      }
    } catch {
      onError('Server unreachable');
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

  async function chi() {
    if (!gameId) return;
    const options = await getChiOptions(server, gameId, playerIndex, log);
    if (!options || options.length === 0) {
      onError('No chi options');
      return;
    }
    if (options.length === 1) {
      simple('chi', { tiles: options[0] });
    } else {
      setChiOptions(options);
    }
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

  function chooseChi(pair) {
    simple('chi', { tiles: pair });
    setChiOptions(null);
  }

  const active =
    (playerIndex === activePlayer || waitingForClaims.includes(playerIndex)) &&
    !aiActive;
  const isAllowed = (action) =>
    active &&
    allowedActions.includes(action) &&
    (action !== 'skip' || waitingForClaims.length > 0);

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
      <ChiModal
        options={chiOptions || []}
        discard={lastDiscard}
        onSelect={chooseChi}
        onClose={() => setChiOptions(null)}
      />
    </div>
  );
}

export default React.memo(Controls);

