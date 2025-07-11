import { formatEvent, eventToMjaiJson } from './eventLog.js';
import { getNextActions } from './nextActions.js';
import { getClaimOptions } from './claimOptions.js';

export async function logNextActions(
  server,
  gameId,
  log = () => {},
  addEvent,
  opts = {},
) {
  const data = await getNextActions(server, gameId, log, opts);
  if (!data || data.aborted) return;
  const evt = { name: 'next_actions', payload: data };
  log('info', formatEvent(evt));
  addEvent(`${formatEvent(evt)} ${eventToMjaiJson(evt)}`);
}

export async function logClaims(
  server,
  gameId,
  log = () => {},
  addEvent,
  opts = {},
) {
  const data = await getClaimOptions(server, gameId, log, opts);
  if (!data || data.aborted) return;
  const evt = { name: 'claims', payload: { claims: data } };
  log('info', formatEvent(evt));
  addEvent(`${formatEvent(evt)} ${eventToMjaiJson(evt)}`);
}
