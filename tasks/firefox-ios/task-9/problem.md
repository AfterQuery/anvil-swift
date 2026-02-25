## Bugfix: Open Relay email mask management page in a new browser tab

### Problem Description

In **Firefox iOS**, tapping "Manage email masks" in the Relay settings opens the management page in an embedded web view within the settings screen. Because the web view is transient, its session cookies are lost when the user quits and relaunches the app. This forces users to log in again every time they want to manage their email masks.

### Acceptance Criteria

1. Tapping "Manage email masks" must open the Relay account management page in a new browser tab rather than in an embedded web view within settings.
2. After opening the tab, the settings screen must be dismissed so the user is taken directly to the new tab.
3. The Relay settings screen must have access to the browser's tab management so it can open new tabs.
4. Existing Relay settings functionality (toggle, section layout) must be preserved.
