# UI components fail to adapt correctly to orientation changes on iPad

## Description
In the **iOS-Open-GPX-Tracker** application, there is a regression/persistent bug regarding how the UI handles device orientation changes, specifically on iPad. While the map itself may rotate, the overlaying UI elements (the button bar, compass, and status labels) do not maintain their intended layout, leading to "squashed" or overlapping components.

## Observed Behavior
- **Button Bar Overlap**: When transitioning between portrait and landscape on an iPad, the bottom button bar (containing "Start Tracking," "Save," and "Reset") fails to recalculate its spacing. This results in buttons overlapping or becoming too compressed to use.  
- **Compass Misalignment**: The compass view moves out of its designated position upon rotation, sometimes disappearing or floating in incorrect coordinates.  
- **Label Truncation**: Status labels (such as the time and coordinate labels at the top) may truncate or have incorrect padding/distance from the edges when the width of the view changes.  
- **Static Layout**: The current implementation relies on manual frame calculations or insufficient checks (like `IsIPhoneX`) that don't account for the dynamic size classes of the iPad.  

## Expected Behavior
- The UI should be robust against width and height changes.  
- The button bar should use flexible constraints to ensure buttons are evenly spaced and never overlap, regardless of orientation.  
- The compass and top status bar labels should remain anchored to their relative positions.  
- UI updates should be triggered correctly during `viewWillTransition(to:with:)` without requiring arbitrary delays.  

## Technical Constraints
- The fix should ideally move away from hardcoded frame math towards `NSLayoutConstraints` to handle different screen sizes (iPad Pro 10.5", iPhone X, etc.) natively.  
- Ensure that the `viewWillTransition` logic is clean and does not introduce unnecessary `DispatchQueue` delays unless absolutely required by the UIKit lifecycle.