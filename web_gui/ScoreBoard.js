import React from 'react';

export default function ScoreBoard({ players = [] }) {
  const winds = ['South', 'West', 'North', 'East'];
  return React.createElement(
    'div',
    { className: 'score-board' },
    winds.map((wind, i) => {
      const p = players[i];
      return React.createElement(
        'div',
        { key: wind, className: 'score-entry' },
        React.createElement('span', { className: 'seat-wind' }, wind),
        React.createElement('span', { className: 'player-name' }, p?.name ?? wind),
        React.createElement('span', { className: 'player-score' }, p?.score ?? 0),
      );
    }),
  );
}
