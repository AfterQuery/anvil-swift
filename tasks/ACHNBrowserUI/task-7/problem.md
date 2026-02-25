## Feature: Add Turnip Exchange listings and improve catalog navigation

### Problem Description

The **ACHNBrowserUI** app does not expose Turnip Exchange island listings anywhere in the UI, even though a `TurnipExchangeService` exists to fetch the data. Users must leave the app to check turnip market opportunities.

Additionally, catalog browsing is fragmented across multiple top-level tabs (Items, Wardrobe, Nature), each using a modal category picker. This flat structure makes it difficult to explore items across category groups and doesn't scale as new sections are added.

### Acceptance Criteria

1. Users can access a Turnips section from the main tab navigation.
2. The section displays island listings fetched from the Turnip Exchange service, with a loading state while data is unavailable.
3. Catalog browsing supports hierarchical drill-down navigation across category groups from a single tab.
4. Individual item lists can be reached by navigating through category groups.
5. The island model handles missing descriptions gracefully.
6. Existing functionality (villagers, collection) remains intact.
7. The app builds and runs without regressions.

### Xcode Project Note

This is a traditional Xcode project (not SwiftPM). New `.swift` files must be registered in `project.pbxproj` or they will not compile.
