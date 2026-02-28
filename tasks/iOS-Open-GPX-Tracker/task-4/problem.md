## Bug: UI components fail to adapt correctly to orientation changes on iPad

### Problem Description

In the **iOS-Open-GPX-Tracker** app, there is a bug regarding how the UI handles device orientation changes on iPad. While the map itself rotates correctly, the overlaying UI elements do not maintain their intended layout, leading to visual issues.

### Observed Behavior

- **Button Bar Overlap**: When transitioning between portrait and landscape on iPad, the bottom button bar fails to recalculate its spacing, resulting in buttons overlapping or becoming too compressed.
- **Compass Misalignment**: The compass view moves out of its designated position upon rotation.
- **Label Truncation**: Status labels may truncate or have incorrect padding when the width changes.

### Acceptance Criteria

1. UI elements must adapt dynamically to size and orientation changes.
2. Buttons, labels, and the compass must maintain correct positions and spacing across orientation transitions.
3. The layout must work correctly across different screen sizes (iPad Pro, iPhone X+, etc.).
4. The view controller must update layout when orientation changes.

### Required API Surface

The implementation must expose this name (tests depend on it to compile):

- `ViewController.addConstraints(_ isIPhoneX: Bool)`
