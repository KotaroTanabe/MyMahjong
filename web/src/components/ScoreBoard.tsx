import { Tile, type Wind } from '@mymahjong/core';
import { TileImage } from './TileImage.js';

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
            <td>
              <TileImage tile={new Tile({ suit: 'wind', value: s.wind })} />
            </td>
            <td>{s.points}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
