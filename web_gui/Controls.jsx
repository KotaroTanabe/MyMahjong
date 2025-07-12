import React, { useState } from 'react';
import Button from './Button.jsx';
import ChiModal from './ChiModal.jsx';
import { getChiOptions } from './chiOptions.js';
import { postAction } from './postAction.js';

export function Controls({
  server,
  gameId,
  playerIndex = 0,
  activePlayer = null,
  aiActive = false,
  allowedActions = [],
  waitingForClaims = [],
  waitingForRiichi = false,
  lastDiscard = null,
  log = () => {},
  onError = () => {},
  onRiichi = null,
  selectingRiichi = false,
}) {
  const [message, setMessage] = useState('');
  const [chiOptions, setChiOptions] = useState(null);


  async function simple(action, payload = {}) {
    log(
      'debug',
      `POST /games/${gameId}/action ${action} ${JSON.stringify(payload)} - control button`,
    );
    const ok = await postAction(
      server,
      gameId,
      { player_index: playerIndex, action, ...payload },
      log,
      onError,
    );
    if (ok) setMessage(action);
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
    if (!lastDiscard) return;
    const tile = { suit: lastDiscard.suit, value: lastDiscard.value };
    simple('pon', { tiles: [tile, tile, tile] });
  }

  function kan() {
    simple('kan', { tiles: [{ suit: 'sou', value: 2 }, { suit: 'sou', value: 2 }, { suit: 'sou', value: 2 }, { suit: 'sou', value: 2 }] });
  }

  function riichi() {
    if (onRiichi) {
      onRiichi();
    } else {
      simple('riichi');
    }
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

  if (selectingRiichi && playerIndex === activePlayer) {
    return <div className="controls">Select tile for riichi</div>;
  }

  if (waitingForRiichi && playerIndex === activePlayer) {
    return (
      <div className="controls">
        <Button onClick={riichi}>Riichi</Button>
        <Button onClick={skip}>Skip</Button>
      </div>
    );
  }

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

