## Feature: Per-tab persistence of homepage vertical scroll position

### Problem Description

In **Firefox iOS**, the homepage does not maintain the vertical scroll position when users switch between tabs or navigate away and return. The homepage always resets to the top, which is disruptive when users have scrolled down to browse content like the Stories section (especially in the vertical stories scroll-direction experiment).

### Acceptance Criteria

1. The homepage must preserve the vertical scroll position per tab — each tab should independently remember where the user was scrolled.
2. When returning to a tab's homepage (by navigating back or switching tabs), the scroll position must be restored to where the user left off.
3. Scroll positions are stored in memory only and do not persist across app sessions.
4. When no saved scroll position exists for a tab (e.g., a new tab), the homepage scrolls to the top as before.
5. Triggering impression tracking must not force the homepage to scroll to the top — impressions should reflect whatever content is currently visible.
6. Impression tracking must fire when the user stops scrolling, whether from a flick-and-decelerate or a drag-and-release.
7. Scrolling to the top must correctly account for content insets so the view is not incorrectly offset.
