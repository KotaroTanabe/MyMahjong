import React from 'react';
import Button from './Button.jsx';
import { FiCopy } from 'react-icons/fi';

export default function EventLogModal({ events, onClose, onCopy }) {
  return (
    <div className="modal is-active">
      <div className="modal-background" onClick={onClose}></div>
      <div className="modal-content">
        <div className="box event-log">
          <div className="event-log-header">
            <h2>Events</h2>
            <Button aria-label="Copy events" onClick={onCopy}>
              <FiCopy />
            </Button>
          </div>
          <ul>
            {events.map((e, i) => (
              <li key={i}>{e}</li>
            ))}
          </ul>
        </div>
      </div>
      <button className="modal-close is-large" aria-label="close" onClick={onClose}></button>
    </div>
  );
}
