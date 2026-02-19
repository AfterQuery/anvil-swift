## Feature: Add a map scale indicator and fix deprecated location authorization check

### Problem Description

The **iOS-Open-GPX-Tracker** map view currently has no scale indicator, making it difficult for users to judge distances on the map. Users need a visual reference that updates as they zoom in and out.

Additionally, the location authorization check uses the deprecated `CLLocationManager.authorizationStatus()` class method. Since iOS 14, the preferred approach is to use the instance-level `locationManager.authorizationStatus` property instead.

### Acceptance Criteria

1. A scale bar using MapKit's built-in `MKScaleView` must be added to the map view and displayed on screen.
2. The scale bar must be linked to the existing map so it automatically updates as the user zooms in and out.
3. All calls to the deprecated `CLLocationManager.authorizationStatus()` class method must be replaced with the instance-level `locationManager.authorizationStatus` property.
4. Obsolete `#available(iOS 10, *)` checks that are no longer needed given the app's current minimum deployment target must be removed.
5. The user-facing alert behavior must remain the same.
