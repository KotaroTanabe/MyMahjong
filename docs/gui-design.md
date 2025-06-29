# GUI Design Philosophy

This document summarizes the ongoing discussion about how to present the Mahjong board in a clear and intuitive manner. The goal is a layout that stays within typical desktop resolutions and also adapts to phone screens in landscape mode.

## Key Ideas

- **Minimal text** – Use tile images or simple icons instead of words wherever possible so players understand the state at a glance.
- **Stable layout** – Reserve space for each player area so the board does not shift when hands or discard piles grow.
- **Responsive grid** – Keep all components visible on common PC screens and introduce media queries to reposition elements for narrow displays.
- **Compact controls** – Replace text buttons with small icons (with tooltips) to reduce clutter.
- **Relative units** – Size elements with `rem` and `%` so they scale naturally when the viewport changes.
  The stylesheet now avoids fixed pixel values; breakpoints and border widths use `rem` units to scale with the root font size.

## Implementation Tasks

1. Provide visual assets for tiles and update the React components to render images instead of text.
2. Update `web/src/style.css` to define fixed or minimum heights for board rows and make player areas scroll if content overflows.
3. Add media queries that reorganize the grid on small screens (e.g. stacking side players above the center).
4. Replace textual control labels with icons and add appropriate `aria-label` attributes.
5. Ensure the layout uses flexible units so it remains usable on both desktops and phones.
6. Show dora indicators and remaining wall tiles in the center display. **Done.**

These tasks will gradually evolve the prototype toward a more intuitive and responsive interface.
