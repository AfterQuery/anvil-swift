## Feature: Auto-recover last track on launch with toast notifications

### Problem Description

In the **iOS-Open-GPX-Tracker** app, when a previously recorded session is recovered from Core Data upon launch, the app presents a blocking dialog asking the user whether to continue the session. This interrupts the startup flow, especially for users who always want to resume tracking.

Additionally, the app has no lightweight, non-intrusive notification system for informing users about transient events (like file recovery, errors, or successful saves). All user feedback relies on modal alert dialogs, which require explicit dismissal.

### Expected Behavior

- When the app launches and detects a recoverable session, it automatically loads the session without presenting a dialog.
- A non-blocking toast notification briefly appears informing the user that the previous session was recovered.
- A reusable toast notification system is available with multiple severity levels and auto-dismissal.
- The app title bar updates to display the current session filename instead of always showing the default app title.
- The app title reverts to the default when the session is reset.

### Acceptance Criteria

1. Recoverable sessions load automatically on launch without a confirmation dialog — the blocking recovery dialog must be removed.
2. A toast notification informs the user of the automatic recovery.
3. The toast system supports multiple severity levels with distinct styling, and each toast must be visible on screen.
4. The app title label reflects the current session filename.
5. The app builds and runs without regressions.

### Required API Surface

The implementation must expose these names (tests depend on them to compile):

- `Toast` — `regular(_:)`, `info(_:)`, `warning(_:)`, `success(_:)`, `error(_:)`
- `Toast.Position` — `.bottom`, `.center`, `.top`
- `Toast.kDelayShort`, `Toast.kDelayLong`
- `ToastLabel(text:)`
- `kAppTitle`
- `ViewController.lastGpxFilename`, `ViewController.appTitleLabel`
- `CoreDataAlertView` must be **deleted**