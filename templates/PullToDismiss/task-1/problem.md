# Add Edge Shadow Effect

## Problem

The pull-to-dismiss gesture currently only supports background effects (shadow/blur) but doesn't cast any shadow from the view itself. This makes the gesture feel flat and less polished.

## Feature Request

Add an edge shadow effect that appears on the view being dismissed, creating depth and making the pull gesture more visually appealing.

**Expected behavior:**

- Shadow should appear at the top edge of the view
- Shadow opacity should increase gradually as the user pulls down (0% → 100%)
- Shadow should fade out when the gesture completes or is cancelled
- Should be configurable (opacity, radius, color, offset) with reasonable defaults

**Example usage:**

```swift
let pullToDismiss = PullToDismiss(scrollView: tableView)

// Use default shadow
pullToDismiss?.edgeShadow = EdgeShadow.default

// Or customize
pullToDismiss?.edgeShadow = EdgeShadow(
    opacity: 0.8,
    radius: 8.0,
    color: .darkGray,
    offset: CGSize(width: 0, height: -10)
)

// Disable if needed
pullToDismiss?.edgeShadow = nil
```

**Notes:**

- Should work alongside existing background effects
- Use CALayer shadow properties for performance
- Shadow intensity should scale with pull progress (similar to how background effects work)
