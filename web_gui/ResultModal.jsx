import React from 'react';
import Hand from './Hand.jsx';
import { tileToEmoji } from './tileUtils.js';
import Button from './Button.jsx';

export default function ResultModal({
  result,
  onClose,
  onCopyLog,
  onShowLog,
  onDownloadTenhou,
  onDownloadMjai,
}) {
  if (!result) return null;
  const { type, scores } = result;
  return (
    <div className="modal is-active">
      <div className="modal-background" onClick={onClose}></div>
      <div className="modal-content">
        <div className="box">
          {type === 'ryukyoku' ? (
            <>
              <p>{result.reason === 'wall_empty' ? 'Exhaustive draw' : 'Draw'}</p>
              {Array.isArray(scores) && (
                <ul>
                  {scores.map((s, i) => (
                    <li key={i}>
                      Player {i + 1}: {s} {result.tenpai?.[i] ? '(tenpai)' : ''}
                    </li>
                  ))}
                </ul>
              )}
            </>
          ) : type === 'end_game' ? (
            <>
              <p>Game over{result.reason ? ` (${result.reason})` : ''}</p>
              {Array.isArray(scores) && (
                <ul>
                  {scores.map((s, i) => (
                    <li key={i}>Player {i + 1}: {s}</li>
                  ))}
                </ul>
              )}
            </>
          ) : (
            <>
              <p>
                Player {result.player_index + 1}{' '}
                {type === 'tsumo' ? 'wins by tsumo' : 'wins by ron'}{' '}
                {result.win_tile ? tileToEmoji(result.win_tile) : ''}
              </p>
              {result.hand && <Hand tiles={result.hand.tiles} />}
              {result.result && (
                <p>
                  {result.result.han} han {result.result.fu} fu –{' '}
                  {result.result.cost?.total ?? 0} points
                </p>
              )}
              {Array.isArray(scores) && (
                <ul>
                  {scores.map((s, i) => (
                    <li key={i}>Player {i + 1}: {s}</li>
                  ))}
                </ul>
              )}
            </>
          )}
          {(onShowLog || onCopyLog || onDownloadMjai || onDownloadTenhou) && (
            <div className="field is-grouped mt-2">
              {onShowLog && (
                <div className="control">
                  <Button aria-label="Show log" onClick={onShowLog}>
                    Log
                  </Button>
                </div>
              )}
              {onCopyLog && (
                <div className="control">
                  <Button onClick={onCopyLog}>Copy Log</Button>
                </div>
              )}
              {onDownloadMjai && (
                <div className="control">
                  <Button aria-label="Download MJAI log" onClick={onDownloadMjai}>
                    MJAI
                  </Button>
                </div>
              )}
              {onDownloadTenhou && (
                <div className="control">
                  <Button aria-label="Download Tenhou log" onClick={onDownloadTenhou}>
                    Tenhou
                  </Button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
      <button
        className="modal-close is-large"
        aria-label="close"
        onClick={onClose}
      ></button>
    </div>
  );
}
