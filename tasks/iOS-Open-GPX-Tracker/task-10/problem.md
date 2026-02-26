## Feature: Add custom output folder selection for GPX files

### Problem Description

The **iOS-Open-GPX-Tracker** app saves all recorded GPX files to the app's internal Documents directory. There is no way for users to choose a different storage location. Users who want their tracks saved to a cloud-synced folder (e.g., iCloud Drive, Dropbox) or a specific local directory must manually move files after each recording session.

### Expected Behavior

- A new "GPX Files Location" section appears in the preferences screen, allowing users to select a custom output folder.
- Tapping the preference opens a system folder picker (`UIDocumentPickerViewController`) so users can choose any accessible local or cloud directory.
- Once a custom folder is selected, the preference cell displays the chosen folder's name.
- If no custom folder is selected, the cell indicates the default folder is in use.
- The selected folder is persisted across app launches so the app retains access to the chosen directory.
- The GPX file list aggregates files from both the default Documents directory and the custom folder (if set), sorted by modification date.
- New GPX files are saved to the custom folder when one is set.
- New localization strings are added for the section header and cell labels (translations were added for English and Russian only; other locales remain untranslated per project convention of requiring human translators).

### Acceptance Criteria

1. A "GPX Files Location" section is visible at the bottom of the preferences table.
2. Selecting a folder via the document picker persists the choice and updates the cell's subtitle.
3. The file list includes GPX files from both the default and custom directories.
4. The preference survives app restarts via bookmark data in UserDefaults.
5. The app builds and runs without regressions.

### Required API Surface

The implementation must expose these names (tests depend on them to compile):

- `kDefaultsKeyGPXFilesFolder` — string constant.
- `Preferences.shared.gpxFilesFolderURL` — optional `URL?` property.
- `kGPXFilesLocationSection` — integer constant.
- `PreferencesTableViewController` must conform to `UIDocumentPickerDelegate`.