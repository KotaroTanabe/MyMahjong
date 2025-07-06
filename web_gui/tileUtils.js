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

export function sortTiles(tiles) {
  const order = { man: 0, pin: 1, sou: 2, wind: 3, dragon: 4 };
  return tiles
    .slice()
    .sort((a, b) => {
      const suitDiff = order[a.suit] - order[b.suit];
      if (suitDiff !== 0) return suitDiff;
      return a.value - b.value;
    });
}

export function sortTilesExceptLast(tiles) {
  if (tiles.length <= 1) return tiles.slice();
  const head = sortTiles(tiles.slice(0, -1));
  head.push(tiles[tiles.length - 1]);
  return head;
}
