import { formatEvent, eventToMjaiJson } from './eventLog.js';
import { getNextActions } from './nextActions.js';

export async function logNextActions(server, gameId, log = () => {}, addEvent) {
  const data = await getNextActions(server, gameId, log);
  if (!data) return;
  const evt = { name: 'next_actions', payload: data };
  log('info', formatEvent(evt));
  addEvent(`${formatEvent(evt)} ${eventToMjaiJson(evt)}`);
}
