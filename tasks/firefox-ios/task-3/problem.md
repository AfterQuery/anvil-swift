## Refactor: Replace SnapKit constraints with NSLayoutConstraint for BrowserViewController header

### Problem Description

In **Firefox iOS**, the `BrowserViewController` uses SnapKit (a third-party library) for its header layout constraints. The project is migrating away from SnapKit to reduce third-party dependencies and improve maintainability. The header layout constraints need to be replaced with native `NSLayoutConstraint` implementations.

### Acceptance Criteria

1. The header layout in `BrowserViewController` must use native `NSLayoutConstraint` instead of SnapKit.
2. The header position and size must continue to adapt correctly based on search bar placement (top vs. bottom) and trait collection changes.
3. Dynamic constraint updates (e.g., during scrolling or toolbar show/hide) must continue to work correctly after the migration.
4. A compatibility layer must exist to allow the SnapKit-to-native migration to proceed incrementally without breaking existing scroll behavior that reads or writes constraint offsets.
5. Visual layout behavior must remain identical to the current SnapKit implementation across all device sizes and orientations.
6. Accessibility (Dynamic Text, VoiceOver) must be preserved.
