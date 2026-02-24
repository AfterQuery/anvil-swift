## Feature: Add creator and custom design tracking to the Collection tab

### Problem Description

The **ACHNBrowserUI** app has no way for users to save and organize Animal Crossing custom design codes (creator codes like `MA-XXXX-XXXX-XXXX` and item codes like `MO-XXXX-XXXX-XXXX`). Players frequently share these codes online and need a place to store them within the app.

Additionally, the Collection tab's segmented picker currently has four top-level segments (Items, Villagers, Critters, Lists). Adding more segments causes label truncation on smaller screens. The "Critters" section is also redundant since critter data is already featured on the Dashboard. The navigation structure needs to be reorganized to accommodate new collection categories without overcrowding the picker.

### Expected Behavior

- Users can add custom designs with a name, code, and description through a form.
- Design codes are validated against the `MA`/`MO` format before saving.
- Saved designs appear in a dedicated list within the Collection tab, showing formatted codes and a creator/item category label.
- Users can delete saved designs.
- The Collection tab's top-level picker is simplified to accommodate the new category without truncating on small screens. Critters and designs should be accessible via a secondary navigation point.
- Empty collection states display a helpful message to the user.
- All design data persists across app launches.
- Existing collection features (items, villagers, lists) remain functional.

### Acceptance Criteria

1. Users can create, view, and delete custom design entries with name, code, and description.
2. Design codes are validated and formatted to the Nintendo `XX-XXXX-XXXX-XXXX` pattern.
3. The Collection picker no longer truncates on small screens.
4. Critters and designs are accessible via a secondary navigation point within Collection.
5. The app builds and runs without regressions.

### API Compatibility Requirements

The test suite expects the following symbols and signatures:

- `Design`: an `Identifiable`, `Equatable` model with `title`, `code`, `description` string properties and a `hasValidCode` computed property.
- `UserCollection.shared.designs`: a `[Design]` published property.
- `DesignFormViewModel(design:)`: an `ObservableObject` accepting an optional `Design`.
- `DesignRowViewModel(design:)`: a struct exposing `title`, `code`, `category`, and `description`.
- `CollectionMoreDetailViewModel()`: a struct with a `rows` property and a `Row` enum with `.critters` and `.designs` cases.
- `Tabs.more`: a case in the collection tab enumeration.
- `MessageView`: a view with `init(string:)`, `init(collectionName:)`, and `init(noResultsFor:)` initializers.

### Xcode Project Note

This is a traditional Xcode project (not SwiftPM). New `.swift` files must be registered in `project.pbxproj` or they will not compile.
