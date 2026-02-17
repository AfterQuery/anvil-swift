## Feature: Implement "Partial Like" State and Variant Selection for Items

### Problem Description

In the **ACHNBrowserUI** app, the "Like" (star) system for items is binary: an item is either liked or not. However, many items in the catalog have multiple color or style variants. Users have no way to see if they have collected **some, but not all, variants** of a specific item directly from the UI. Additionally, tapping the favorite button on an item with variants simply toggles the parent item rather than letting users select specific variants.

This makes it difficult for users to track per-variant collection progress.

### Expected Behavior

The like system should support three states based on variant completion:

1. **Unstarted** — zero variants liked (no star).
2. **Partially liked** — at least one variant liked, but not all (half-star icon).
3. **Fully liked** — all variants liked (full star).

This requires:

- Updating `UserCollection` backend logic to track variant completion status and determine the correct state.
- Automatically syncing the parent item's liked status with its variants: the parent item should be added to the collection when the first variant is liked, and removed when the last variant is unliked.
- Displaying a "half-star" icon in the UI to represent the partially liked state, updating dynamically when variants are toggled.
- When a user taps the favorite button on an item with variants, presenting a bottom sheet for selecting individual variants (with smooth animations for presentation and dismissal).
- Ensuring the favorite button in the **ItemDetail** navigation bar triggers the same variant selection bottom sheet.

### Constraints

- The existing like behavior for items without variants should remain unchanged.
- The half-star icon state should update immediately when variants are toggled in the bottom sheet.
- Do not change the behavior of other collection tracking features.

### Requirements

- Liking one variant of an item with multiple variants should set the completion status to **partial**.
- Liking all variants of an item should set the completion status to **complete**.
- Unliking all variants should reset the completion status to **unstarted**.
- Liking the first variant of an item should automatically add the parent item to the collection.
- Unliking the last variant of an item should automatically remove the parent item from the collection.
- Items with only one variant (or no variants) should not use the partial like system.
