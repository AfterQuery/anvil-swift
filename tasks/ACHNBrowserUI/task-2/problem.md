## Fix: Improve Alignment and Grid Layout for Turnip Price Predictions

### Problem Description

In the **ACHNBrowserUI** app, the Turnips price prediction section displays daily AM/PM price estimates using separate row view structs (`TurnipsAveragePriceRow`, `TurnipsMinMaxPriceRow`, `TurnipsPriceRow`) that each define their own `HStack` layout. Because each row independently positions its columns with `Spacer()`, the AM and PM values do not align cleanly across rows, creating a jagged or "staircase" visual effect.

### Expected Behavior

The turnip price grid should use a unified grid layout component (e.g., a custom `GridStack` using row/column indices) so that:

1. **Horizontal Alignment**: AM and PM columns are consistently aligned under their headers across all rows.
2. **Vertical Spacing**: Consistent row height and dividers between the days of the week.
3. **Code Simplification**: The separate row view files and the `eraseToAnyViewForRow()` workaround should be removed, replaced by a single grid component used for all three display modes (average prices, min/max prices, and profits).

### Constraints

- The grid layout must be used for all three display modes (average, min/max, profits) — not just one.
- The old row view files (`TurnipsAveragePriceRow.swift`, `TurnipsMinMaxPriceRow.swift`, `TurnipsPriceRow.swift`) and the `rows/` directory should be removed entirely.
- The `eraseToAnyViewForRow()` helper on `View` should be removed since the grid handles row layout directly.
- Do not change the chart views, island views, or other unrelated sections of the turnip price screen.
