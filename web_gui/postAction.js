export async function postAction(server, gameId, body, log = () => {}, onError = () => {}, retries = 0) {
  const url = `${server.replace(/\/$/, '')}/games/${gameId}/action`;
  try {
    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (resp.ok) return true;
    let msg = `Action ${body.action} failed: ${resp.status}`;
    let detail = null;
    try {
      const data = await resp.json();
      if (data.detail) detail = data.detail;
    } catch {}
    if (detail) msg = detail;
    log('warn', msg);
    if (resp.status === 409 && retries < 3) {
      try {
        const nextResp = await fetch(`${server.replace(/\/$/, '')}/games/${gameId}/next-actions`);
        if (nextResp.ok) {
          const next = await nextResp.json();
          if (next && next.actions && next.actions.length > 0 && next.player_index != null) {
            let nextBody = { player_index: next.player_index, action: next.actions[0] };
            if (nextBody.action === 'discard' || nextBody.action === 'riichi') {
              nextBody = { player_index: next.player_index, action: 'auto', ai_type: 'simple' };
            }
            log('debug', `Retrying with ${JSON.stringify(nextBody)}`);
            return postAction(server, gameId, nextBody, log, onError, retries + 1);
          }
        }
      } catch {}
    }
    onError(msg);
  } catch {
    onError('Failed to contact server');
  }
  return false;
}
