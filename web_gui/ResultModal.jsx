import React from 'react';

export default function ResultModal({ result, onClose }) {
  if (!result) return null;
  const { scores, tenpai, reason } = result;
  return (
    <div className="modal is-active">
      <div className="modal-background" onClick={onClose}></div>
      <div className="modal-content">
        <div className="box">
          <p>{reason === 'wall_empty' ? 'Exhaustive draw' : 'Draw'}</p>
          {Array.isArray(scores) && (
            <ul>
              {scores.map((s, i) => (
                <li key={i}>
                  Player {i + 1}: {s} {tenpai?.[i] ? '(tenpai)' : ''}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
      <button className="modal-close is-large" aria-label="close" onClick={onClose}></button>
    </div>
  );
}
