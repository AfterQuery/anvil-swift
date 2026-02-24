## Feature: Add Turnip Exchange listings and improve catalog navigation

### Problem Description

The **ACHNBrowserUI** app does not expose Turnip Exchange island listings anywhere in the UI, even though a `TurnipExchangeService` exists to fetch the data. Users must leave the app to check turnip market opportunities.

Additionally, catalog browsing is fragmented across multiple top-level tabs (Items, Wardrobe, Nature), each using a modal category picker. This flat structure makes it difficult to explore items across category groups and doesn't scale as new sections are added.

### Expected Behavior

- Users can access a Turnips section from the main tab navigation.
- The section displays island listings fetched from the Turnip Exchange service.
- Listings load asynchronously and show a loading state while data is unavailable.
- Catalog browsing supports hierarchical drill-down navigation across category groups from a single tab.
- Individual item lists can be reached by navigating through category groups.
- The `Island` model handles missing descriptions gracefully.
- Existing functionality (villagers, collection) remains intact.

### Acceptance Criteria

1. Turnip Exchange island listings are visible within the app via the main navigation.
2. Listings update when data is fetched.
3. Catalog navigation supports structured, hierarchical browsing.
4. The app builds and runs without regressions.

### API Compatibility Requirements

The test suite expects the following symbols and signatures:

- `TurnipsViewModel`: an `ObservableObject` with a `@Published var islands: [Island]?` property (nil by default) and a `func fetch()` method.
- `TabbarView.Tab.turnips`: a case in the tab enumeration.
- `Island`: conforms to `Identifiable`.
- `CategoriesView(categories:)`: initializer accepting `[Categories]` with no additional binding parameter.
- `CategoryDetailView(categories:)`: initializer accepting `[Categories]`.
- `ItemsListView(viewModel:)`: initializer accepting an `ItemsViewModel`.
- `ItemsViewModel(categorie:)`: initializer must be accessible from outside its defining file.

### Xcode Project Note

This is a traditional Xcode project (not SwiftPM). New `.swift` files must be registered in `project.pbxproj` or they will not compile.
