## Feature: Add custom output folder selection for GPX files

### Problem Description

The **iOS-Open-GPX-Tracker** app saves all recorded GPX files to the app's internal Documents directory. There is no way for users to choose a different storage location. Users who want their tracks saved to a cloud-synced folder (e.g., iCloud Drive, Dropbox) or a specific local directory must manually move files after each recording session.

### Expected Behavior

- A new "GPX Files Location" section appears in the preferences screen, allowing users to select a custom output folder.
- Tapping the preference opens a system folder picker so users can choose any accessible directory.
- Once a custom folder is selected, the preference cell displays the chosen folder's name.
- The selected folder is persisted across app launches.
- The GPX file list aggregates files from both the default and custom directories.
- New GPX files are saved to the custom folder when one is set.

### Acceptance Criteria

1. A "GPX Files Location" section is visible in the preferences table.
2. Selecting a folder persists the choice and updates the cell's subtitle.
3. The file list includes GPX files from both the default and custom directories.
4. The preference survives app restarts.
5. The app builds and runs without regressions.

### Required API Surface

The implementation must expose these names (tests depend on them to compile):

- `kDefaultsKeyGPXFilesFolder`
- `Preferences.shared.gpxFilesFolderURL`
- `kGPXFilesLocationSection`
- `PreferencesTableViewController` — UIDocumentPickerDelegate