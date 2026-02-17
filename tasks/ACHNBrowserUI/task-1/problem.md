## Feature: Add "To Catch Now" section to Active Critters view

### Problem Description

In the **ACHNBrowserUI** app, the Active Critters view currently shows a single "To Catch" section that lists all critters available during the current month. Users have to manually scan through the entire list to figure out which critters are actually catchable at the current hour, since many critters are only active during specific time windows within the day.

This makes it difficult for users to quickly identify what they should be looking for right now.

### Expected Behavior

The "To Catch" section should be split into two separate sections:

1. **To Catch Now** — critters that are available at the current hour.
2. **To Catch Later** — critters that are available this month but not at the current time.

This requires:

- Extracting active hour information from each item's time data to determine if a critter is currently catchable.
- Updating `ActiveCrittersView` to display the new `toCatchNow` and `toCatchLater` collections as separate sections.
- Handling all critter types (fish, bugs) consistently.

### Constraints

- Edge cases such as empty collections should be handled gracefully (sections should not appear if empty).
- The existing "To Catch" logic should be preserved for the "Later" section.
- Do not change the behavior of other sections in the Active Critters view.
