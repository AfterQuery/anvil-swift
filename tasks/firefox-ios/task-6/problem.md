## Refactor: Improve skeleton address bar performance for tab swiping

### Problem Description

In **Firefox iOS**, the skeleton (placeholder) address bars shown during the swipe-to-switch-tab gesture use the full configuration method on the address toolbar. This method sets up delegates, gesture recognizers, accessibility, keyboard configuration, and other interactive features that are unnecessary for non-interactive skeleton bars. The overhead degrades swiping performance.

Additionally, the skeleton bars do not show site-security indicators (shield icons), and the swipe gesture lacks a minimum horizontal-distance threshold, which can cause unintended tab switches during vertical scrolling.

### Acceptance Criteria

1. A lightweight, non-interactive configuration path exists for skeleton address bars that skips delegates, gestures, accessibility, keyboard, and position/border setup.
2. Skeleton bar configuration can derive site-security status directly from a tab (rather than requiring separate URL and reader-mode parameters).
3. Skeleton bars display a shield icon when the tab's content is served over a secure connection.
4. Reader-mode URLs hide the lock icon in skeleton bars.
5. A minimum horizontal swipe distance is required before a fast-swipe triggers a tab transition, preventing accidental switches during vertical scrolling.
6. The full interactive configuration method is no longer part of the public API.
