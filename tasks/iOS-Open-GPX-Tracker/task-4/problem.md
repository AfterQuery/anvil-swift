## Bug: UI components fail to adapt correctly to orientation changes on iPad

### Problem Description

In the **iOS-Open-GPX-Tracker** app, there is a bug regarding how the UI handles device orientation changes on iPad. While the map itself rotates correctly, the overlaying UI elements do not maintain their intended layout, leading to visual issues.

### Observed Behavior

- **Button Bar Overlap**: When transitioning between portrait and landscape on iPad, the bottom button bar (containing "Start Tracking," "Save," and "Reset") fails to recalculate its spacing, resulting in buttons overlapping or becoming too compressed to use.
- **Compass Misalignment**: The compass view moves out of its designated position upon rotation, sometimes disappearing or floating at incorrect coordinates.
- **Label Truncation**: Status labels (such as the time and coordinate labels at the top) may truncate or have incorrect padding from the edges when the width changes.
- **Static Layout**: The current implementation relies on manual frame calculations and device-specific checks (like `IsIPhoneX`) that don't account for the dynamic size classes of various iPad models.

### Acceptance Criteria

1. The layout must be migrated from manual frame calculations and `autoresizingMask` to Auto Layout constraints so that all UI elements adapt dynamically to size changes.
2. Buttons must not use hardcoded frame or center assignments — their positions must be defined by constraints relative to the view.
3. Status labels must not use hardcoded frame assignments — they must remain anchored to their relative positions as the view resizes.
4. The view controller must respond to orientation transitions and update the layout accordingly, without requiring arbitrary delays.
5. The compass must reposition correctly when the orientation changes, remaining in its designated location.
6. The layout must work correctly across different screen sizes (including iPad Pro models and iPhone X+) without device-specific conditionals.
