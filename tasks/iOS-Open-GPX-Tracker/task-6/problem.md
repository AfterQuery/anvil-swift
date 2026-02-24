## Fix: Auto-reload file list when GPX files are received externally

### Problem Description

In the **iOS-Open-GPX-Tracker** app, when a user receives a GPX file via AirDrop or from the paired Apple Watch while the file list view is open, the table view does not update to show the new file. The user must close and reopen the file list to see it. Additionally, WatchConnectivity session management is handled in the ViewController, which means file transfers from the Apple Watch cannot be processed when the app is in the background or the main view controller is not active.

### Expected Behavior

- When a GPX file is received via AirDrop (URL import), the file list table view automatically reloads to show the new file.
- When a GPX file is received from the Apple Watch, the file list table view automatically reloads and an alert notifies the user of the received file.
- WatchConnectivity session activation is handled at the app delegate level so file transfers work regardless of which view is active.
- The main view controller no longer manages WCSession directly.
- Notification-based communication is used to decouple file reception events from specific view controllers.

### Acceptance Criteria

1. The file list updates immediately when a file arrives via AirDrop or Apple Watch transfer.
2. WCSession delegation is handled by the AppDelegate, not the ViewController.
3. The ViewController displays an alert when a file is received from Apple Watch.
4. The app builds and runs without regressions.

### API Compatibility Requirements

The test suite expects the following symbols and signatures:

- `Notification.Name.didReceiveFileFromURL`: a static notification name.
- `Notification.Name.didReceiveFileFromAppleWatch`: a static notification name.
- `GPXFilesTableViewController` responds to `reloadTableData` selector.
- `ViewController` does not conform to `WCSessionDelegate`.
