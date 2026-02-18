## Feature: Add Sorting Options to Villagers List

### Problem Description

In the **ACHNBrowserUI** app, the Villagers list view displays all villagers but provides no way to sort them. Users who want to find villagers by name or browse by species have to manually scan through the entire unsorted list.

This makes it difficult for users to organize and browse the villager catalog efficiently.

### Expected Behavior

The Villagers list should support sorting by **name** and **species**, accessible via a sort button in the navigation bar:

1. **Sort by Name** — villagers sorted alphabetically by their localized name.
2. **Sort by Species** — villagers sorted alphabetically by species.

This requires:

- Adding a `Sort` enum and sorting logic to `VillagersViewModel`, with a `sortedVillagers` published property that the view consumes.
- Tapping the same sort option a second time should reverse the sort order (ascending to descending).
- Creating a `VillagersSortView` that presents an action sheet with the available sort options, a "Clear Selection" option when a sort is active, and a cancel button.
- The sort button icon in the navigation bar should visually indicate whether a sort is active (e.g., filled vs outline icon).
- The villagers list should display `sortedVillagers` when a sort is active, `searchResults` when searching, and the default `villagers` list otherwise.
- French localization should be added for the "Sort villagers" action sheet title.

### Constraints

- The existing search functionality should remain unchanged and take priority over sorting (search results are not sorted).
- Clearing the sort selection should restore the original villager order.
- Do not change the behavior of other views or the villager detail view.

### Requirements

- Selecting "Name" sort should return villagers sorted alphabetically by localized name in ascending order.
- Selecting "Name" sort a second time should reverse to descending order.
- Selecting "Species" sort should return villagers sorted alphabetically by species in ascending order.
- Selecting "Species" sort a second time should reverse to descending order.
- Clearing the sort selection should reset `sortedVillagers` to an empty list, causing the view to fall back to the default villager order.
- When a sort is active, the sort button icon should use the filled variant.
- When no sort is active, the sort button icon should use the outline variant.
