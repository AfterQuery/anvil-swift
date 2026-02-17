## Bug: Scalebar color not correctly adapting to tile server background

### Problem Description

The map scalebar color is currently determined using the system appearance mode (dark vs. light). Specifically:

- **White** is used in dark mode  
- **Black** is used in light mode  

However, this behavior leads to poor visibility when certain tile providers are used, because their map backgrounds do not match the system appearance.

### Incorrect Behavior

The scalebar color is not legible in the following cases:

#### Apple Satellite tiles
- The imagery is dark.  
- The scalebar becomes black in light mode, making it difficult to see.  
- **Expected:** scalebar should always be **white**.

#### OpenStreetMap and similar light-themed tiles
- The imagery is light.  
- The scalebar becomes white in dark mode, reducing contrast.  
- **Expected:** scalebar should always be **black**.

### Expected Behavior

The scalebar color should adapt to the tile provider rather than the system appearance.