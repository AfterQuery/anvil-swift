### Title
Replace deprecated UIAlertView usage with UIAlertController

### Background
The application currently uses `UIAlertView` to present alerts to users. `UIAlertView` has been deprecated since iOS 9 and is no longer supported in modern iOS development practices.

Apple recommends using `UIAlertController` with `preferredStyle: .alert` or `.actionSheet` to present alerts.

Continuing to use deprecated APIs may cause compatibility issues, warnings during compilation, and potential runtime problems on newer iOS versions.

### Current Behavior
The codebase still contains usages of:

- `UIAlertView`
- delegate-based alert handling
- `show()` calls on alert views

These APIs are deprecated and should no longer be used.

### Expected Behavior
All alert dialogs should be presented using `UIAlertController`, ensuring:

- compatibility with modern iOS versions
- proper presentation via a view controller
- replacement of delegate-based callbacks with action handlers

### Constraints
- Do not change user-facing behavior.
- Do not introduce deprecated APIs.
- Ensure alerts are presented on the main thread.
- Maintain compatibility with the app’s current navigation structure.
