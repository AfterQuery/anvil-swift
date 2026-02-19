## Feature: Persist homepage vertical scroll position per tab

### Problem Description

In **Firefox iOS**, the homepage does not maintain the vertical scroll position when users switch between tabs or navigate away and back. The homepage always resets to the top, which is disruptive when users have scrolled down to browse content like the Stories section.

### Acceptance Criteria

1. The homepage must preserve the vertical scroll position per tab — each tab should independently remember where the user was scrolled.
2. When returning to a tab's homepage (by navigating back or switching tabs), the scroll position must be restored to where the user left off.
3. Scroll positions must not be persisted across app sessions — they exist in memory only.
4. When no saved scroll position exists for a tab (e.g., a new tab), the homepage should scroll to the top as before.
5. Triggering impression tracking must not force the homepage to scroll to the top — impressions should reflect whatever content is currently visible.
6. Impression tracking must fire whenever the user stops scrolling, whether that results from a flick-and-decelerate or a drag-and-release.
7. Scrolling to the top must correctly account for content insets so the view is not incorrectly offset.
8. This feature applies when the homepage stories scroll direction experiment is customized on iPhone.
