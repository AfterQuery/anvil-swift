## Modernization: Replace deprecated UIAlertView usage with UIAlertController

### Problem Description

The **iOS-Open-GPX-Tracker** application uses `UIAlertView` to present alert dialogs in several places (e.g., saving a GPX session, editing waypoint names, location services denied/disabled alerts). `UIAlertView` has been deprecated since iOS 9 and is no longer supported in modern iOS development. Continuing to use it can cause compatibility issues, compiler warnings, and runtime problems on newer iOS versions.

### Acceptance Criteria

1. `UIAlertView` and `UIAlertViewDelegate` must not appear anywhere in the codebase.
2. All alert functionality must be preserved using the modern `UIAlertController` API.
3. All user-facing behavior and messaging must remain the same (same titles, messages, button labels, and actions).
4. Alerts must be presented from the appropriate view controller within the current navigation flow.
5. Existing alert-presenting methods (e.g., `displayLocationServicesDisabledAlert`) must remain on `ViewController` — they must be migrated in place, not deleted.
