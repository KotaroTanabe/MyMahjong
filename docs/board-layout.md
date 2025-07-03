# Board Layout Details

This document outlines how the Mahjong board is arranged in the web UI. The design follows the conventions of a physical table while making small adjustments for digital screens.

## Orientation

- The local player's hand is shown along the bottom edge.
- Tiles within each hand are laid out horizontally, matching a traditional table view.
- Each player's discard pile (河) sits directly in front of their hand. For the bottom player this means discards appear above the hand.
- Discards are grouped into rows of six to form a compact river. The `DiscardPile` component adds orientation classes so each seat's river aligns toward the center of the table.
- Melded tiles (calls such as chi or pon) are displayed at the four corners of the table so discard piles remain clearly separated.
- Opponents occupy the top, left and right edges, surrounding a central area used for wall tiles or indicators.

### Layout Example

The following ASCII diagram shows the relative placement of each player's discard pile (河)
and open melds (鳴). Melds sit in the four corners while the wall and dora indicators occupy
the center:

```
  +---------------+---------------+---------------+
  | NW Fuuro      | North River    | NE Fuuro      |
  +---------------+---------------+---------------+
  | West River    | Wall & Dora    | East River    |
  +---------------+---------------+---------------+
  | SW Fuuro      | South River    | SE Fuuro      |
  +---------------+---------------+---------------+
```

Discard piles surround the center while each player's opened sets cluster in the
corners. The central area holds the remaining wall tiles and dora indicator display.

## Digital Considerations

To conserve screen space the interface avoids lengthy text and uses small buttons or icons. The layout reserves fixed regions for each player so elements do not jump as the game progresses. Media queries can stack the side players vertically when the viewport becomes narrow, ensuring controls remain accessible on phones.
The discard areas maintain a minimum height so a player's hand does not shift even when no tiles have been discarded.
This is enforced via the `.discard-pile` CSS rule which now reserves enough space for four rows (24 tiles).

### Meld Buttons

The bottom player area now includes small "Pon", "Chi", "Kan" and "Ron" buttons beneath the hand. These trigger calls on the most recent discard from the right-hand opponent. Future versions may allow targeting any discard or provide icon-based controls.

These guidelines provide a baseline for implementing responsive components in the `web` package.
