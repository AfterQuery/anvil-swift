### Title
Homepage loses scroll position when returning from a story while vertical stories experiment is enabled

### Background
The homepage includes a Stories section that can be configured via a feature flag to scroll vertically through all fetched stories (up to 100). When the `stories-scroll-direction` experiment is set to `vertical`, the homepage uses a vertically scrolling list and hides access to the full stories feed view.

The Stories section appears near the bottom of the homepage and partially “peeks” below the fold.

### Feature Flag
stories-scroll-direction: vertical  
homepage-redesign-feature: enabled

### Current Behavior
When a user:
1. Opens the homepage with vertical stories enabled.
2. Scrolls down to the Stories section.
3. Opens a story.
4. Navigates back to the homepage using the toolbar back button.

The homepage resets to the top instead of restoring the previous scroll position.

### Expected Behavior
Returning from a story should restore the homepage to its previous scroll offset, preserving the user’s position within the vertically scrolling stories section.

### Constraints & Notes
- Applies only when vertical stories mode is enabled.
- iPhone-only layout.
- Stories section uses the homepage diffable data source and layout provider.
- Vertical mode removes the fixed section height calculation and relies on dynamic layout sizing.
- The issue likely involves:
  - layout invalidation or content offset restoration,
  - data source reload behavior,
  - view lifecycle handling when returning from navigation.

### Task
Modify the homepage layout or navigation restoration logic so that returning from a story preserves the previous scroll position when vertical stories mode is enabled.
