## Fix: Relay email mask management page should open in a browser tab

### Problem Description

In **Firefox iOS**, the Relay email mask management page currently opens in an embedded web view within the settings screen. This causes users to lose their session cookies when they quit and relaunch the app, requiring them to log in again each time they want to manage their email masks.

### Acceptance Criteria

1. Tapping "Manage email masks" must open the Relay account management page in a new browser tab rather than in an embedded web view within settings.
2. After opening the tab, the settings screen must be dismissed so the user is taken directly to the new tab.
3. The Relay settings screen must have access to the browser's tab management so it can open new tabs.
4. Unit tests must be added to verify: there are no memory leaks, the settings screen produces the expected configuration, the correct URL is used, and tapping the manage option results in a new tab being opened.
5. Existing functionality of other settings must remain unaffected.
