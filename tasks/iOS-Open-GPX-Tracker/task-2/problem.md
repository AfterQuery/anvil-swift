## Feature: Add localization support for internationalization

### Problem Description

The **iOS-Open-GPX-Tracker** app contains hard-coded user-facing strings throughout the codebase. Button labels, alert messages, screen titles, and other text are embedded directly in the source code. This prevents the app from being translated into other languages and blocks community contributions for localization.

### Expected Behavior

- All user-facing strings in the iOS app and Apple Watch extension support translation.
- The app displays text according to the user's device language when a translation is available.
- Buttons and labels accommodate longer translated text without layout issues.

### Acceptance Criteria

1. User-facing strings in view controllers, alerts, and the Watch extension are localizable.
2. At least one additional language is supported alongside English.
3. The app builds and runs without regressions.

### Required API Surface

The implementation must expose these names (tests depend on them to compile):

- `kNoFiles`
- `kNotGettingLocationText`
