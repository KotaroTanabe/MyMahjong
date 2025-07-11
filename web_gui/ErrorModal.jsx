import React from 'react';
import { FiRefreshCw } from 'react-icons/fi';
import Button from './Button.jsx';

export default function ErrorModal({ message, onClose, onRetry = null }) {
  return (
    <div className={`modal ${message ? 'is-active' : ''}`}>
      <div className="modal-background" onClick={onClose}></div>
      <div className="modal-content">
        <div className="box">
          <p>{message}</p>
          {onRetry && (
            <div className="has-text-centered mt-2">
              <Button
                aria-label="Retry"
                onClick={() => {
                  onClose();
                  onRetry();
                }}
              >
                <FiRefreshCw />
              </Button>
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
