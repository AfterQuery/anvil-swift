## Feature: Custom output folder for GPX files

### Problem Description

In the **iOS-Open-GPX-Tracker** app, all saved GPX files are stored in the app's default Documents directory. Users have no way to specify a different folder for GPX file output, such as a shared iCloud Drive folder or an external storage location. This makes it difficult to organize tracks across multiple apps or access them from a file manager.

### Acceptance Criteria

1. A new "GPX Files Location" section appears at the bottom of the preferences screen.
2. Tapping the row presents a system folder picker that allows the user to select a custom folder.
3. The selected folder persists across app launches via a security-scoped bookmark stored in UserDefaults.
4. The file list screen shows GPX files from both the default Documents directory and the custom folder, sorted by modification date.
5. When a custom folder is set, GPX files are saved there; when cleared, the app reverts to the default Documents directory.
6. The selected folder name is displayed as the detail text in the preferences row.
