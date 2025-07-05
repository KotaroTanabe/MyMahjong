export function tileToEmoji(tile) {
  const { suit, value } = tile;
  if (suit === 'man') {
    return String.fromCodePoint(0x1f007 + (value - 1));
  }
  if (suit === 'sou') {
    return String.fromCodePoint(0x1f010 + (value - 1));
  }
  if (suit === 'pin') {
    return String.fromCodePoint(0x1f019 + (value - 1));
  }
  if (suit === 'wind') {
    return String.fromCodePoint(0x1f000 + (value - 1));
  }
  if (suit === 'dragon') {
    return String.fromCodePoint(0x1f004 + (value - 1));
  }
  return `${suit[0]}${value}`;
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
