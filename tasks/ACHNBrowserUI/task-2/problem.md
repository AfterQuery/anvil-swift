## Fix: Turnip price columns are misaligned across rows

### Problem Description

In the **ACHNBrowserUI** app, the Turnips price prediction section displays daily AM/PM price estimates. Each row in the table independently positions its columns, which causes the AM and PM values to not align vertically across rows. This creates a jagged, hard-to-read layout.

The misalignment affects all three display modes: average prices, min/max prices, and profits.

### Acceptance Criteria

1. The AM and PM columns must be consistently aligned under their headers across all rows using a unified grid or column-aligned layout.
2. The unified layout must be used for all three display modes (average, min/max, profits).
3. The old separate row view files in the `rows/` directory must be removed, along with any references to those components from the turnip price view.
4. Any workarounds that existed solely to support the old row-based layout should be removed.
5. Do not change the chart views, island views, or other unrelated sections of the turnip price screen.
6. Implement the unified layout as a reusable grid view in the shared views directory with configurable row/column counts and optional spacing.

### Xcode Project Note

This is a traditional Xcode project (not SwiftPM). When you add or remove `.swift` files, you must also update `project.pbxproj` to register/unregister them in the build target. Files that exist on disk but are not listed in the Xcode project will not be compiled.
