## Feature: Add sorting options to the Villagers list

### Problem Description

In the **ACHNBrowserUI** app, the Villagers list view displays all villagers but provides no way to sort them. Users who want to find villagers by name or browse by species have to manually scan through the entire unsorted list.

### Acceptance Criteria

1. Users must be able to sort villagers by name (alphabetical by localized name) and by species (alphabetical).
2. Sorting must use locale-aware string comparison.
3. A sort button in the navigation bar must present the available sort options (e.g., via an action sheet).
4. The sort button icon must visually indicate whether a sort is currently active.
5. Selecting the same sort option a second time must reverse the sort order.
6. There must be a way to clear the active sort, restoring the default villager order.
7. When searching, search results must take priority over sorting.
8. French localization must be added for any new user-facing sort strings.
9. The existing search functionality and villager detail view must remain unchanged.
10. Add sort state to `VillagersViewModel` (e.g., a `Sort` enum and a `sortedVillagers` array) so the view can bind to it.
