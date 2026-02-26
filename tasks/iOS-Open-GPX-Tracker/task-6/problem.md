## Fix: Auto-reload file list when GPX files are received externally

### Problem Description

In the **iOS-Open-GPX-Tracker** app, when a user receives a GPX file via AirDrop or from the paired Apple Watch while the file list view is open, the table view does not update to show the new file. The user must close and reopen the file list to see it. Additionally, WatchConnectivity session management is handled in the ViewController, which means file transfers from the Apple Watch cannot be processed when the app is in the background or the main view controller is not active.

### Expected Behavior

- When a GPX file is received via AirDrop (URL import), the file list table view automatically reloads to show the new file.
- When a GPX file is received from the Apple Watch, the file list table view automatically reloads and an alert notifies the user of the received file.
- File transfers from the Apple Watch work regardless of which view is active.
- The main view controller no longer manages WCSession directly.

### Acceptance Criteria

1. The file list updates immediately when a file arrives via AirDrop or Apple Watch transfer.
2. WCSession delegation is moved out of the ViewController.
3. The user is notified when a file is received from Apple Watch.
4. The app builds and runs without regressions.

### Required API Surface

The implementation must expose these names (tests depend on them to compile):

- `Notification.Name.didReceiveFileFromURL` — static extension on `Notification.Name`.
- `Notification.Name.didReceiveFileFromAppleWatch` — static extension on `Notification.Name`.
- `GPXFilesTableViewController.reloadTableData()` — instance method (must be `@objc`) to refresh the file list table. The controller must observe both notification names and call this method when they fire.
- `AppDelegate` must conform to `WCSessionDelegate` and implement `session(_:didReceive:)` for Apple Watch file transfers.