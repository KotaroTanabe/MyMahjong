# Board Layout Details

This document outlines how the Mahjong board is arranged in the web UI. The design follows the conventions of a physical table while making small adjustments for digital screens.

## Orientation

- The local player's hand is shown along the bottom edge.
- Each player's discard pile (河) sits directly in front of their hand. For the bottom player this means discards appear above the hand.
- Melded tiles (calls such as chi or pon) align to the right of that player's discard pile. This keeps the main hand centered while revealing open sets.
- Opponents occupy the top, left and right edges, surrounding a central area used for wall tiles or indicators.

## Digital Considerations

To conserve screen space the interface avoids lengthy text and uses small buttons or icons. The layout reserves fixed regions for each player so elements do not jump as the game progresses. Media queries can stack the side players vertically when the viewport becomes narrow, ensuring controls remain accessible on phones.

These guidelines provide a baseline for implementing responsive components in the `web` package.
