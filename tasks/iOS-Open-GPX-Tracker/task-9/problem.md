## Feature: Add activity type selection to preferences

### Problem Description

The **iOS-Open-GPX-Tracker** app uses `CLLocationManager` for GPS tracking but does not expose the `activityType` setting to users. The location manager defaults to `.other` (automatic), which may not produce optimal tracking accuracy for specific activities like driving, running, or flying. Users have no way to tell the system what kind of activity they are performing to improve GPS filtering behavior.

### Expected Behavior

- A new "Activity Type" section appears in the preferences screen listing all available activity type options.
- Each option displays a human-readable name and a brief description.
- The currently selected activity type is indicated with a checkmark.
- Selecting a different activity type persists the choice and updates the location manager.
- The preference is saved and restored on app launch.

### Acceptance Criteria

1. An "Activity Type" section is visible in the preferences table.
2. All activity type options are listed with names and descriptions.
3. Tapping a row updates the checkmark and persists the selection.
4. The location manager uses the selected activity type for tracking.
5. The app builds and runs without regressions.

### Required API Surface

The implementation must expose these names (tests depend on them to compile):

- `CLActivityType.name`, `CLActivityType.description`, `CLActivityType.count`
- `kActivityTypeSection`
- `kDefaultsKeyActivityType`
- `Preferences.shared.locationActivityType`