## Feature: Add a map scale indicator and clean up obsolete version checks

### Problem Description

The **iOS-Open-GPX-Tracker** map view currently has no scale indicator, making it difficult for users to judge distances on the map. Users need a visual reference that updates as they zoom in and out.

Additionally, the codebase contains obsolete `#available(iOS 10, *)` version checks that are no longer needed given the app's current minimum deployment target.

### Acceptance Criteria

1. A scale bar using MapKit's built-in `MKScaleView` must be added to the map view and displayed on screen.
2. The scale bar must be linked to the existing map so it automatically updates as the user zooms in and out.
3. Obsolete `#available(iOS 10, *)` checks that are no longer needed given the app's current minimum deployment target must be removed.
4. The user-facing alert behavior must remain the same.

### Required API Surface

The implementation must expose these specific names (tests depend on them):

- `ViewController.scaleBar` — stored property of type `MKScaleView` on `ViewController`.
