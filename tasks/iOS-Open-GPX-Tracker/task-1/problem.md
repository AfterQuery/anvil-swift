## Bug: Scalebar and label colors not adapting to tile server background

### Problem Description

In the **iOS-Open-GPX-Tracker** app, the map overlay text (status labels) and the custom scalebar determine their color based on whether the system is in dark mode or light mode. However, different tile servers have inherently dark or light map imagery regardless of the system appearance setting, which makes the overlay elements hard to read in certain combinations.

For example:
- **Apple Satellite** tiles have dark imagery, but in light mode the scalebar and labels are black — nearly invisible against the dark map.
- **OpenStreetMap** and similar tiles have light imagery, but in dark mode the scalebar and labels are white — washed out against the light map.

### Acceptance Criteria

1. The scalebar must support having its color overridden based on the tile server, rather than always using system-adaptive colors.
2. The tile server selection must drive the scalebar's color — when the user switches tile servers, the scalebar color must update accordingly.
3. Dark-themed tile servers (e.g., Apple Satellite) must use white overlay elements (scalebar, labels).
4. Light-themed tile servers (e.g., OpenStreetMap) must use black overlay elements.
5. The default Apple map tile server should continue to follow the system appearance mode.

### Required API Surface

The implementation must expose these names (tests depend on them to compile):

- `GPXTileServer.GPXTileServerColorMode` — nested enum with cases `.lightMode`, `.system`, `.darkMode`.
- `GPXTileServer.colorMode` — computed property returning `GPXTileServerColorMode`.
- `GPXScaleBar.forcedColor` — optional `UIColor?` property.