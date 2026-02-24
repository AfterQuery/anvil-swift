## Feature: Add activity type selection to preferences

### Problem Description

The **iOS-Open-GPX-Tracker** app uses `CLLocationManager` for GPS tracking but does not expose the `activityType` setting to users. The location manager defaults to `.other` (automatic), which may not produce optimal tracking accuracy for specific activities like driving, running, or flying. Users have no way to tell the system what kind of activity they are performing to improve GPS filtering behavior.

### Expected Behavior

- A new "Activity Type" section appears in the preferences screen listing all available `CLActivityType` options (Automatic, Automotive navigation, Fitness, Other navigation, Flight).
- Each option displays a human-readable name and a brief description of the activity.
- The currently selected activity type is indicated with a checkmark.
- Selecting a different activity type persists the choice and notifies the main view controller to update the location manager.
- The preference is saved to UserDefaults and restored on app launch.

### Acceptance Criteria

1. An "Activity Type" section is visible in the preferences table.
2. All five `CLActivityType` options are listed with names and descriptions.
3. Tapping a row updates the checkmark and persists the selection.
4. The location manager uses the selected activity type for tracking.
5. The app builds and runs without regressions.

### API Compatibility Requirements

The test suite expects the following symbols and signatures:

- `CLActivityType.name`: a computed `String` property returning a human-readable name.
- `CLActivityType.description`: a computed `String` property returning a brief description.
- `CLActivityType.count`: a static `Int` property returning `5`.
- `kActivityTypeSection`: an `Int` constant for the activity type section index.
- `kDefaultsKeyActivityType`: a `String` constant for the UserDefaults key.
- `Preferences.shared.locationActivityType`: a read/write `CLActivityType` property.
- `numberOfSections(in:)` on `PreferencesTableViewController` returns `4` (increased from `3`).
