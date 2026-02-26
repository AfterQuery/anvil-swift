## Feature: "Screen always on" preference and loading indicator for preferences screen

### Problem Description

The **iOS-Open-GPX-Tracker** app has two user-facing issues related to preferences and screen behavior:

1. **No "keep screen on" option.** When tracking a route, the device screen dims and locks after the system idle timeout. Users lose sight of the live map and must repeatedly wake the device to check their position. There is no in-app setting to prevent this.

2. **Preferences screen appears to hang.** Opening the preferences screen calculates the tile cache size synchronously on the main thread. When the cache is large (e.g., 1 GB), this blocks the UI for several seconds with no visual feedback, making users think the button did nothing.

### Expected Behavior

- A "Keep screen always on" toggle is available in the app's preferences under a new "Screen" section.
- When enabled, the device screen stays on while the app is in the foreground.
- The preference persists across app launches and is applied when the app starts.
- Opening the preferences screen shows a loading toast while the view controller initializes, so the user gets immediate feedback even if initialization is slow.
- The loading toast disappears once the preferences screen is ready to present.
- New preference strings ("Screen" section header and "Keep screen always on" label) are localized for all supported languages.

### Acceptance Criteria

1. A new preferences section for screen behavior is visible in the preferences table.
2. Toggling the setting keeps the screen awake or restores default idle timer behavior.
3. The preference is persisted to UserDefaults and restored on app launch.
4. A loading indicator appears while the preferences screen loads and disappears once it is presented.
5. The app builds and runs without regressions.

### Required API Surface

The implementation must expose these names (tests depend on them to compile):

- `Preferences.shared.keepScreenAlwaysOn` — `Bool` property.
- `kDefaultsKeyKeepScreenAlwaysOn` — string constant.
- `kScreenSection` — new integer constant for the screen preferences section (must precede the existing `kCacheSection`).
- `Toast.kDisabledDelay` — static `Double` constant with a negative sentinel value indicating a persistent toast that should not auto-dismiss.
- `Toast.showLoading(_: String)` — static method.
- `Toast.hideLoading()` — static method.