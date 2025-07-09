import React from 'react';
import Hand from './Hand.jsx';
import { tileToEmoji } from './tileUtils.js';

export default function ResultModal({ result, onClose, onCopyLog }) {
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
          {onCopyLog && (
            <button className="button mt-2" onClick={onCopyLog}>
              Copy Log
            </button>
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
