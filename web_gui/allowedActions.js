const controllers = new Map();

export function cleanupAllowedActions() {
  for (const controller of controllers.values()) {
    controller.abort();
  }
  controllers.clear();
}

function prepareSignal(id, signal) {
  if (!id) {
    console.warn('getAllowedActions requires a requestId');
    return signal;
  }
  if (signal) return signal;
  const prev = controllers.get(id);
  if (prev) prev.abort();
  const controller = new AbortController();
  controllers.set(id, controller);
  return controller.signal;
}

export async function getAllowedActions(
  server,
  gameId,
  playerIndex,
  log = () => {},
  { signal, requestId } = {},
) {
  const finalSignal = prepareSignal(requestId, signal);
  try {
    const url = `${server.replace(/\/$/, '')}/games/${gameId}/allowed-actions/${playerIndex}`;
    log('debug', `GET ${url} - update allowed actions`);
    const resp = await fetch(url, { signal: finalSignal });
    if (!resp.ok) {
      return { error: `HTTP ${resp.status}` };
    }
    const data = await resp.json();
    return data.actions || [];
  } catch (err) {
    if (err.name === 'AbortError') return { aborted: true };
    return { error: err.message };
  } finally {
    if (requestId) controllers.delete(requestId);
  }
}

export async function getAllAllowedActions(
  server,
  gameId,
  log = () => {},
  { signal, requestId } = {},
) {
  const finalSignal = prepareSignal(requestId, signal);
  try {
    const url = `${server.replace(/\/$/, '')}/games/${gameId}/allowed-actions`;
    log('debug', `GET ${url} - fetch allowed actions`);
    const resp = await fetch(url, { signal: finalSignal });
    if (!resp.ok) {
      return { error: `HTTP ${resp.status}` };
    }
    const data = await resp.json();
    return data.actions || [];
  } catch (err) {
    if (err.name === 'AbortError') return { aborted: true };
    return { error: err.message };
  } finally {
    if (requestId) controllers.delete(requestId);
  }
}

export function applyAllowedActionsEvent(current, event) {
  if (event?.name === 'allowed_actions' && Array.isArray(event.payload?.actions)) {
    return event.payload.actions;
  }
  return current;
}
