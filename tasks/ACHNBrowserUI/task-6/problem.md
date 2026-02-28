## Feature: Add a Dashboard view summarizing game progress and marketplace activity

### Problem Description

The **ACHNBrowserUI** app has no centralized overview of the player's progress. Users must navigate between multiple tabs to check critter collection status, turnip prices, or marketplace listings. There is no single screen that aggregates this information, and the app opens to the Catalog tab by default.

### Expected Behavior

- A Dashboard screen is accessible from the app's main tab navigation and serves as the default landing view.
- The dashboard displays active critter counts, collection progress for fish/bugs/fossils, the top Turnip Exchange island listing, and recent Nookazon marketplace listings.
- All data loads asynchronously with appropriate loading states.
- Existing features (catalog, turnips, villagers, collection) remain fully functional.

### Acceptance Criteria

1. A Dashboard view is visible in the main tab navigation as the first and default tab.
2. Critter counts and collection progress render correctly from existing data models and services.
3. Turnip island and marketplace listings populate using existing services.
4. The app builds and runs without regressions.

### Required API Surface

The implementation must expose these names (tests depend on them to compile):

- `DashboardViewModel` — ObservableObject; `recentListings`, `island`, `fishes`, `bugs`, `fossils`, `fetchListings()`, `fetchIsland()`, `fetchCritters()`
- `TabbarView.Tab.dashboard`
- `Categories.fish()`, `Categories.bugs()`
- `Listing.name`, `Listing.img`
- `NookazonService.recentListings()`

### Xcode Project Note

This is a traditional Xcode project (not SwiftPM). New `.swift` files must be registered in `project.pbxproj` or they will not compile.
