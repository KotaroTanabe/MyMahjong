import type { Wind } from '@mymahjong/core';

export interface ScoreBoardProps {
  scores: { wind: Wind; points: number }[];
}

export function ScoreBoard({ scores }: ScoreBoardProps): JSX.Element {
  return (
    <table className="scoreboard">
      <thead>
        <tr>
          <th>Wind</th>
          <th>Points</th>
        </tr>
      </thead>
      <tbody>
        {scores.map(s => (
          <tr key={s.wind}>
            <td>{s.wind}</td>
            <td>{s.points}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
