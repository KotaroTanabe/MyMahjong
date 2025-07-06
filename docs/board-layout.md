# Board Layout Details

This document outlines how the Mahjong board is arranged in the web UI. The design follows the conventions of a physical table while making small adjustments for digital screens.

## Orientation

- The local player's hand is shown along the bottom edge.
- Tiles within each hand are laid out horizontally, matching a traditional table view.
- Each player's discard pile (河) sits directly in front of their hand. For the bottom player this means discards appear above the hand.
- Discards are grouped into rows of six to form a compact river. The `DiscardPile` component adds orientation classes so each seat's river aligns toward the center of the table.
- Melded tiles (chi, pon and kan) are shown to the right of each player's hand.
  This follows the common convention where opened sets sit beside the hand.
  Discard piles remain directly in front of the players.
- Opponents occupy the top, left and right edges, surrounding a central area used for wall tiles or indicators.
- Each opponent's concealed hand is drawn just outside their discard pile so the river remains visible.
- Each seat's discard pile and meld area is rotated with CSS so tiles face the center.
  `.seat-east` rotates 90deg, `.seat-north` 180deg and `.seat-west` -90deg.
- Melds are drawn in dedicated areas separate from discard piles so rivers remain intact.

### Player Panel Layout

An alternative layout treats each player area as a self-contained panel:

```
+---------------+---------------------+
| Toimen panel  | Shimocha panel      |
+---------------+---------------------+
| Kamicha panel | Jicha panel (self)  |
+---------------+---------------------+
```

Each panel stacks a thin riichi stick area with the seat name and score, a river
display that grows up to four rows of six tiles, then a combined hand and meld
section. The panels themselves are arranged in a 2x2 grid.

Discard piles surround the center while each player's opened sets cluster in the
corners. The central area holds the remaining wall tiles and dora indicator display.

## Digital Considerations

To conserve screen space the interface avoids lengthy text and uses small buttons or icons. The layout reserves fixed regions for each player so elements do not jump as the game progresses. Media queries can stack the side players vertically when the viewport becomes narrow, ensuring controls remain accessible on phones.
The discard areas maintain a minimum height so a player's hand does not shift even when no tiles have been discarded.
This is enforced via the `.discard-pile` CSS rule which now reserves enough space for four rows (24 tiles).

### Meld Buttons

The bottom player area now includes small "Pon", "Chi", "Kan" and "Ron" buttons beneath the hand. These trigger calls on the most recent discard from the right-hand opponent. Future versions may allow targeting any discard or provide icon-based controls.

These guidelines provide a baseline for implementing responsive components in the `web` package.
