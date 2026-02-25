## Bugfix: Unexpected homepage appearance lifecycle events during swipe-to-new-tab gesture

### Problem Description

In **Firefox iOS**, the homepage is added to the view hierarchy on app launch so that a screenshot can be programmatically captured and used as a preview image when the user swipes to create a new tab. Because the homepage is in the view hierarchy (even when hidden), its lifecycle methods (`viewDidAppear`, etc.) fire unexpectedly, causing:

- Duplicate homepage impression telemetry.
- Unwanted side-effects from lifecycle callbacks that assume the homepage is actively visible to the user.

This was introduced in the "Swipe Tabs gesture — cache homepage" change (PR #27280).

### Acceptance Criteria

1. Launching the app with swiping tabs enabled must not trigger homepage lifecycle events.
2. The swipe-to-new-tab preview shows a placeholder image (e.g., a Firefox favicon) rather than a live homepage screenshot.
3. The content container must always clean up previous non-webview content when adding new content, regardless of device or swiping-tabs state.
4. Any screenshot or homepage-visibility APIs that only existed to support the old caching approach are removed.
5. Homepage impression telemetry must only fire when the homepage is genuinely presented to the user.
