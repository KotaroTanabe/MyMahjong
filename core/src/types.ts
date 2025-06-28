export type NumberSuit = 'man' | 'pin' | 'sou';
export type Wind = 'east' | 'south' | 'west' | 'north';
export type Dragon = 'white' | 'green' | 'red';
export type HonorSuit = 'wind' | 'dragon';
export type Suit = NumberSuit | HonorSuit;

export interface NumberTile {
  suit: NumberSuit;
  value: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;
}

export interface WindTile {
  suit: 'wind';
  value: Wind;
}

export interface DragonTile {
  suit: 'dragon';
  value: Dragon;
}

export type TileType = NumberTile | WindTile | DragonTile;
