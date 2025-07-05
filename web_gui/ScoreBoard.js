import React from 'react';

export default function ScoreBoard({ players = [] }) {
  return React.createElement(
    'div',
    { className: 'score-board' },
    players.map((p, i) =>
      React.createElement(
        'div',
        { key: i, className: 'score-row' },
        React.createElement('span', { className: 'player-name' }, p?.name || `Player ${i}`),
        React.createElement('span', { className: 'player-wind' }, p?.seat_wind),
        React.createElement('span', { className: 'player-score' }, p?.score)
      )
    )
  );
}
