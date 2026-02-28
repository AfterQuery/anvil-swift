## Feature: Custom default file name format in preferences

### Problem Description

The **iOS-Open-GPX-Tracker** app uses a hardcoded date format when generating default file names for saved GPX sessions. Users have no way to customize this format, which is inconvenient for those who prefer ISO 8601 timestamps, 24-hour time, or other naming conventions.

### Expected Behavior

- A new "Default Name" section appears in the preferences table, linking to a dedicated setup screen.
- Users can choose from preset date/time format patterns or enter a custom format string.
- A live preview shows the current date/time rendered in the selected format.
- The selected format persists across app launches and is applied when generating default file names.
- Invalid or malformed patterns are handled gracefully instead of crashing.

### Acceptance Criteria

1. A "Default Name" section is visible in the main preferences table.
2. Preset formats are selectable with a live date/time preview.
3. Custom format input produces correct file names.
4. The app builds and runs without regressions.

### Required API Surface

The implementation must expose these names (tests depend on them to compile):

- `DefaultDateFormat` — `getDateFormat(unprocessed:)`, `getDate(processedFormat:)`
- `DateField` — `type`, `patterns`, `subtitles`
- `String.countInstances(of:)`
- `kDefaultNameSection`
- `DefaultNameSetupViewController`