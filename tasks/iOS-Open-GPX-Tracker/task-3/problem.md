## Title: Add MapKit scale bar and fix location status check warning

### Problem Description

The map view currently has no scale indicator, making it difficult for users to judge distances on the map. MapKit provides `MKScaleView`, a built-in scale bar that automatically updates as the user zooms in and out.

Additionally, the location authorization check in the ViewController uses the deprecated `CLLocationManager.locationServicesEnabled()` class method inside a `guard` statement, which produces a compiler warning on modern iOS versions. The check should use the instance-level `authorizationStatus` property instead.

### Expected Behavior

1. **Scale bar**: An `MKScaleView` should be added to the map view, positioned above the tracker button, and connected to the map so it reflects the current zoom level.

2. **Location status check**: The deprecated `CLLocationManager.locationServicesEnabled()` guard should be replaced with a check on `authorizationStatus` (e.g., checking for `.denied`) to eliminate the compiler warning.

### Constraints

- Use MapKit's built-in `MKScaleView` for the scale bar — do not implement a custom one.
- The scale bar must be linked to the existing map view.
- Do not change user-facing alert behavior.
- Remove any unnecessary iOS version availability checks that are no longer needed (the app's minimum deployment target has moved past them).
