## Fix: Auto-reload file list when GPX files are received externally

### Problem Description

In the **iOS-Open-GPX-Tracker** app, when a user receives a GPX file via AirDrop or from the paired Apple Watch while the file list view is open, the table view does not update to show the new file. The user must close and reopen the file list to see it. Additionally, WatchConnectivity session management is handled in the ViewController, which means file transfers from the Apple Watch cannot be processed when the app is in the background or the main view controller is not active.

### Expected Behavior

- When a GPX file is received via AirDrop or from the Apple Watch, the file list table view automatically reloads to show the new file.
- The user is notified when a file is received from Apple Watch.
- File transfers from the Apple Watch work regardless of which view is active.

### Acceptance Criteria

1. The file list updates immediately when a file arrives via AirDrop or Apple Watch transfer.
2. The user is notified when a file is received from Apple Watch.
3. The app builds and runs without regressions.

### Required API Surface

The implementation must expose these names (tests depend on them to compile):

- `Notification.Name.didReceiveFileFromURL`
- `Notification.Name.didReceiveFileFromAppleWatch`
- `GPXFilesTableViewController.reloadTableData()`
- `AppDelegate` — must conform to `WCSessionDelegate`