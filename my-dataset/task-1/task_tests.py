import glob
import re
from pathlib import Path


def _read_all_swift_sources():
    """Read all Swift files in Sources/ into a single concatenated string.

    This allows tests to find definitions regardless of which file they live in,
    so the model is free to organize code however it sees fit.
    """
    sources = []
    for f in sorted(Path("/app/Sources").glob("*.swift")):
        sources.append(f.read_text())
    return "\n".join(sources)


# ---------------------------------------------------------------------------
# 1. EdgeShadow type definition
#    The model must create an EdgeShadow struct or class somewhere in Sources/.
# ---------------------------------------------------------------------------

def test_edge_shadow_type_exists():
    """An EdgeShadow struct or class must be defined in Sources/."""
    content = _read_all_swift_sources()
    assert re.search(r"(struct|class)\s+EdgeShadow", content), \
        "EdgeShadow struct or class should be defined in Sources/"


def test_edge_shadow_has_required_properties():
    """EdgeShadow must expose opacity, radius, color, and offset properties.

    These are the four configurable shadow parameters mentioned in the
    problem statement's example usage.
    """
    content = _read_all_swift_sources()
    assert "opacity" in content, "EdgeShadow should have opacity property"
    assert "radius" in content, "EdgeShadow should have radius property"
    assert "color" in content, "EdgeShadow should have color property"
    assert "offset" in content, "EdgeShadow should have offset property"


def test_edge_shadow_default_instance():
    """EdgeShadow must provide a static default instance (EdgeShadow.default).

    Accepts both `static let` and `static var` declarations, and handles
    the backtick-escaped `default` keyword in Swift.
    """
    content = _read_all_swift_sources()
    assert re.search(r"(static\s+let|static\s+var)\s+`?default`?", content), \
        "EdgeShadow should have a default static instance"


def test_edge_shadow_is_configurable():
    """EdgeShadow must have an init() so users can pass custom values.

    The problem statement shows: EdgeShadow(opacity: 0.8, radius: 8.0, ...)
    """
    content = _read_all_swift_sources()
    assert re.search(r"init\s*\(", content), \
        "EdgeShadow should have an initializer for custom configuration"


# ---------------------------------------------------------------------------
# 2. Integration into PullToDismiss
#    The model must wire EdgeShadow into the existing drag lifecycle.
# ---------------------------------------------------------------------------

def test_edge_shadow_property_in_pulltodismiss():
    """PullToDismiss must have an `edgeShadow` property (var or let).

    This is the public API shown in the problem statement:
        pullToDismiss?.edgeShadow = EdgeShadow.default
    """
    content = Path("/app/Sources/PullToDismiss.swift").read_text()
    assert "edgeShadow" in content, "PullToDismiss should have edgeShadow property"
    assert re.search(r"(var|let)\s+edgeShadow", content), \
        "edgeShadow should be declared as a property"


def test_edge_shadow_applied_during_drag():
    """Shadow must be applied/updated during the drag gesture.

    We look for the `edgeShadow` property being referenced alongside any
    shadow-related update logic (progress, rate, opacity, apply, update).
    This is intentionally flexible -- the model can use any method names.
    """
    content = Path("/app/Sources/PullToDismiss.swift").read_text()
    has_shadow_in_update = (
        "edgeShadow" in content and
        re.search(r"(shadow|Shadow).*(progress|rate|opacity|apply|update)", content, re.IGNORECASE)
    )
    assert has_shadow_in_update, \
        "Edge shadow should be applied/updated during drag (shadow intensity should scale with progress)"


def test_edge_shadow_reset_on_finish():
    """Shadow must be cleaned up when the drag finishes or is cancelled.

    Accepts any cleanup pattern: setting shadowOpacity to 0, calling a
    detach/remove/reset method, or setting shadow to nil.
    """
    content = Path("/app/Sources/PullToDismiss.swift").read_text()
    has_shadow_cleanup = (
        "edgeShadow" in content and
        re.search(r"(shadow|Shadow).*(0\.?0?|reset|detach|remove|nil)", content, re.IGNORECASE)
    )
    assert has_shadow_cleanup, \
        "Edge shadow should be reset/removed when drag finishes or is cancelled"


# ---------------------------------------------------------------------------
# 3. Performance: CALayer shadow APIs
#    The problem statement says "Use CALayer shadow properties for performance."
# ---------------------------------------------------------------------------

def test_edge_shadow_uses_calayer():
    """Implementation must use CALayer shadow properties (.shadowOpacity, etc.).

    Searches all Sources/ files since the layer manipulation could live in
    EdgeShadow itself, a UIView extension, or directly in PullToDismiss.
    """
    content = _read_all_swift_sources()
    layer_shadow_usage = re.search(r"\.shadow(Opacity|Color|Radius|Offset|Path)", content)
    assert layer_shadow_usage, \
        "Should use CALayer shadow properties (shadowOpacity, shadowColor, etc.) for performance"


# ---------------------------------------------------------------------------
# 4. Regression: don't break existing code
# ---------------------------------------------------------------------------

def test_pullto_dismiss_class_still_exists():
    """PullToDismiss must remain an open class (no accidental deletion)."""
    content = Path("/app/Sources/PullToDismiss.swift").read_text()
    assert "class PullToDismiss" in content, "PullToDismiss class should exist"
    assert "open class PullToDismiss" in content, "PullToDismiss should be open class"
