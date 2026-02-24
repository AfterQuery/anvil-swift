## Feature: Auto-recover last track on launch with toast notifications

### Problem Description

In the **iOS-Open-GPX-Tracker** app, when a previously recorded session is recovered from Core Data upon launch, the app presents a blocking dialog asking the user whether to continue the session. This interrupts the startup flow, especially for users who always want to resume tracking.

Additionally, the app has no lightweight, non-intrusive notification system for informing users about transient events (like file recovery, errors, or successful saves). All user feedback relies on modal alert dialogs, which require explicit dismissal.

### Expected Behavior

- When the app launches and detects a recoverable session, it automatically loads the session without presenting a dialog.
- A non-blocking toast notification briefly appears on screen informing the user that the previous session was recovered.
- A reusable toast notification system is available with multiple severity levels (regular, info, warning, success, error), configurable position (top, center, bottom), and auto-dismissal after a configurable delay.
- The app title bar updates to display the current session filename (truncated if too long) instead of always showing the default app title.
- The app title reverts to the default when the session is reset.

### Acceptance Criteria

1. Recoverable sessions load automatically on launch without a confirmation dialog.
2. A toast notification informs the user of the automatic recovery.
3. The toast system supports multiple severity levels with distinct styling.
4. The app title label reflects the current session filename.
5. The app builds and runs without regressions.

### API Compatibility Requirements

The test suite expects the following symbols and signatures:

- `Toast`: a class with class methods `regular(_:position:delay:)`, `info(_:position:delay:)`, `warning(_:position:delay:)`, `success(_:position:delay:)`, and `error(_:position:delay:)`.
- `Toast.Position`: an enum with cases `.bottom`, `.center`, `.top`.
- `ToastLabel`: a `UILabel` subclass with a `convenience init(text:)` initializer.
- `kAppTitle`: a `String` constant.
