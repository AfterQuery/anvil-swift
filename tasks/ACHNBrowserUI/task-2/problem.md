## Fix: Improve Alignment and Grid Layout for Turnip Price Predictions

### Background

This looks like a classic UI alignment and layout optimization task for the **ACHNBrowserUI** project (an Animal Crossing: New Horizons companion app). In the Turnips section, the **"Daily min-max prices"** grid currently suffers from poor alignment and inconsistent spacing between columns. Specifically:

- AM and PM price values do not align cleanly under their headers.
- The "Day" labels lack proper vertical distribution.

The current implementation uses nested `VStack`/`HStack` or a suboptimal `Grid` approach, making the UI cluttered and difficult to read at a glance.

### Task

Refactor the Turnip price grid to use a more robust layout (e.g., a custom `GridStack` or improved `LazyVGrid` logic) to ensure:

1. **Horizontal Alignment**: AM and PM columns are perfectly centered or consistently aligned under their headers.
2. **Vertical Spacing**: Consistent row height and padding between the days of the week.
3. **Code Simplification**: Remove redundant grid rows or unnecessary nesting that complicates the view hierarchy.

### Evidence

- **Previously**: Monday–Saturday values are offset, creating a "staircase" or jagged visual effect.
- **Proposed**: Values should be neatly organized in a clean table format where headers and data points share the same X-axis coordinates.

### Expected File Changes

- Modify the SwiftUI views responsible for the Turnip price detail screens, especially where the Daily min-max prices section is defined.
- Replace hard-coded offsets or nested stacks with a unified grid component.
