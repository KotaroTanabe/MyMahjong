export function tileToImage(tile) {
  const { suit, value } = tile;
  return `./assets/${suit}_${value}.svg`;
}

export function tileDescription(tile) {
  const { suit, value } = tile;
  if (suit === 'wind') {
    const names = ['east', 'south', 'west', 'north'];
    return `${names[value - 1]} wind`;
  }
  if (suit === 'dragon') {
    const names = ['white', 'green', 'red'];
    return `${names[value - 1]} dragon`;
  }
  return `${value} ${suit}`;
}
