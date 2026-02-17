### Title

Replace deprecated UIAlertView usage with UIAlertController

### Background

The application currently uses `UIAlertView` to present alerts.  
`UIAlertView` has been deprecated since iOS 9 and is no longer supported in modern iOS development.

Apple recommends using `UIAlertController` with `preferredStyle: .alert` or `.actionSheet`.

Continuing to use deprecated APIs can cause compatibility issues, compiler warnings, and runtime problems on newer iOS versions.

### Expected Behavior

All alert dialogs must be presented using `UIAlertController`.

The new implementation should:

- present alerts from a view controller
- use `UIAlertAction` handlers instead of delegate callbacks
- maintain the same user-facing behavior and alert flow

### Requirements

- Remove all usages of `UIAlertView`.
- Present alerts using `UIAlertController`.
- Do not change user-visible behavior or messaging.
- Do not introduce deprecated APIs.
- Ensure alerts are presented within the current navigation flow.
