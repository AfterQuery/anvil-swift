## Feature: Add a map scale indicator and clean up obsolete version checks

### Problem Description

The **iOS-Open-GPX-Tracker** map view currently has no scale indicator, making it difficult for users to judge distances on the map. Users need a visual reference that updates as they zoom in and out.

Additionally, the codebase contains obsolete `#available(iOS 10, *)` version checks that are no longer needed given the app's current minimum deployment target.

### Acceptance Criteria

1. A scale indicator must be visible on the map and update automatically as the user zooms in and out.
2. The indicator must be properly positioned using constraints, not hardcoded frames.
3. Obsolete `#available(iOS 10, *)` checks must be removed.
4. The user-facing alert behavior must remain the same.

### Required API Surface

The implementation must expose these specific names (tests depend on them):

- `ViewController.scaleBar` — stored property of type `MKScaleView` on `ViewController`. Must be connected to the map, added to the view hierarchy, and use Auto Layout.
