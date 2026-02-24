## Feature: Add a Dashboard view summarizing game progress and marketplace activity

### Problem Description

The **ACHNBrowserUI** app has no centralized overview of the player's progress. Users must navigate between multiple tabs to check critter collection status, turnip prices, or marketplace listings. There is no single screen that aggregates this information, and the app opens to the Catalog tab by default.

### Expected Behavior

- A Dashboard screen is accessible from the app's main tab navigation and serves as the default landing view.
- The dashboard displays:
  - Active critter counts (fish and bugs) showing caught vs total, based on the user's hemisphere setting.
  - Collection progress for fish, bugs, and fossils.
  - The top Turnip Exchange island listing.
  - Recent Nookazon marketplace listings with item name, image, and listing details.
- All data loads asynchronously with appropriate loading states.
- Existing features (catalog, turnips, villagers, collection) remain fully functional.
- Reused UI components (turnip cells, listing rows, item images) render correctly when embedded in the new dashboard context.

### Acceptance Criteria

1. A Dashboard view is visible in the main tab navigation as the first and default tab.
2. Critter counts and collection progress render correctly from existing data models and services.
3. Turnip island and marketplace listings populate using existing services.
4. The app builds and runs without regressions.

### Xcode Project Note

This is a traditional Xcode project (not SwiftPM). New `.swift` files must be registered in `project.pbxproj` or they will not compile.
