## Bug: Homepage loses scroll position when returning from a story (vertical stories mode)

### Problem Description

In **Firefox iOS**, the homepage includes a Stories section that can be configured via a feature flag to scroll vertically through all fetched stories (up to 100). When the `stories-scroll-direction` experiment is set to `vertical` (with `homepage-redesign-feature` enabled), the Stories section appears near the bottom of the homepage.

When a user scrolls down to the Stories section, opens a story, and then navigates back to the homepage, the page resets to the top instead of restoring the previous scroll position.

### Feature Flags

- `stories-scroll-direction`: `vertical`
- `homepage-redesign-feature`: `enabled`

### Steps to Reproduce

1. Open the homepage with vertical stories enabled.
2. Scroll down to the Stories section.
3. Open a story.
4. Navigate back to the homepage using the toolbar back button.

**Actual**: The homepage resets to the top.
**Expected**: The homepage restores the previous scroll position.

### Acceptance Criteria

1. When vertical stories mode is enabled on iPhone, stories must scroll vertically in a list rather than horizontally in a carousel.
2. In vertical mode, story cells must be full-width (spanning the content area) rather than narrow horizontal cards.
3. The stories section height must grow dynamically to fit its content rather than being fixed.
4. Scrolling to the top of the homepage must correctly account for adjusted content insets so the view is not offset when reset.
5. Switching between horizontal and vertical story experiments must not cause stale layout measurements to be reused.
6. This behavior applies only when the vertical stories experiment is active on iPhone.
