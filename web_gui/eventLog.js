import { tileDescription } from './tileUtils.js';

export function formatEvent(evt) {
  if (!evt || !evt.name) return '';
  const p = evt.payload?.player_index;
  switch (evt.name) {
    case 'draw_tile':
      return `Player ${p} draws ${tileDescription(evt.payload.tile)}`;
    case 'discard':
      return `Player ${p} discards ${tileDescription(evt.payload.tile)}`;
    case 'meld':
      return `Player ${p} calls ${evt.payload.meld.type}`;
    case 'riichi':
      return `Player ${p} declares riichi`;
    case 'tsumo':
      return `Player ${p} wins by tsumo`;
    case 'ron':
      return `Player ${p} wins by ron`;
    case 'skip':
      return `Player ${p} skips`;
    case 'start_kyoku':
      return `Start hand ${evt.payload.round}`;
    case 'start_game':
      return 'Game started';
    case 'ryukyoku':
      return `Ryukyoku: ${evt.payload.reason}`;
    case 'end_game':
      return 'Game ended';
    default:
      return evt.name;
  }
}

