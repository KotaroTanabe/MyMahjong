import React from 'react';
import { tileToEmoji } from './tileUtils.js';

export default function ChiModal({ options = [], discard = null, onSelect, onClose }) {
  if (!options || options.length === 0) return null;
  function renderMeld(pair) {
    const meld = discard ? [...pair, discard] : pair.slice();
    meld.sort((a, b) => a.value - b.value);
    return meld.map((t, i) => (
      <span key={i} className="mj-tile" aria-hidden="true">
        {tileToEmoji(t)}
      </span>
    ));
  }
  return (
    <div className="modal is-active">
      <div className="modal-background" onClick={onClose}></div>
      <div className="modal-content">
        <div className="box">
          <p>Choose Chi</p>
          {options.map((opt, i) => (
            <button
              key={i}
              className="button m-1"
              aria-label={`chi option ${i}`}
              onClick={() => onSelect?.(opt)}
            >
              {renderMeld(opt)}
            </button>
          ))}
        </div>
      </div>
      <button className="modal-close is-large" aria-label="close" onClick={onClose}></button>
    </div>
  );
}

