## Feature: Custom default file name format in preferences

### Problem Description

The **iOS-Open-GPX-Tracker** app uses a hardcoded date format (`dd-MMM-yyyy-HHmm`) when generating default file names for saved GPX sessions. Users have no way to customize this format, which is inconvenient for those who prefer ISO 8601 timestamps, 24-hour time, or other naming conventions.

### Expected Behavior

- A new "Default Name" section appears in the preferences table, linking to a dedicated setup screen.
- The setup screen provides a list of preset date/time format patterns (e.g., `dd-MMM-yyyy-HHmm`, ISO 8601 variants, 12-hour and 24-hour styles).
- A live preview shows the current date/time rendered in the selected format.
- Users can enter a custom format using `{pattern}` syntax, where patterns follow `DateFormatter` conventions (e.g., `{dd}-{MMM}-{yyyy}`).
- Quick-insert buttons above the keyboard allow inserting common date components (Day, Month, Year, Hour, Min, Sec).
- A scrollable keyboard accessory view provides access to all date pattern fields organized by category.
- Options to force UTC time zone and English locale are available as toggles.
- The selected format and settings persist across app launches.
- The saved format is applied when generating default file names for new GPX sessions.
- Invalid or malformed patterns (e.g., unclosed braces) display an error instead of crashing.

### Acceptance Criteria

1. A "Default Name" section is visible in the main preferences table.
2. Preset formats are selectable with a live date/time preview.
3. Custom format input with `{pattern}` syntax produces correct file names.
4. UTC and English locale toggles work correctly.
5. The app builds and runs without regressions.