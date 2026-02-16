"""Structural tests for GPX-Tracker task-1: Scalebar color adapts to tile server.

These tests verify ONLY what the problem statement requires:
  1. The scale bar must accept an externally-set color (accessible API)
  2. The ViewController must set the scale bar's color based on the tile server
  3. White must be used for dark-themed tiles (e.g. Apple Satellite)
  4. Black must be used for light-themed tiles (e.g. OpenStreetMap)

No specific refactoring approach, enum design, or naming is enforced.
"""

import re
from pathlib import Path

SCALE_BAR = Path("/app/OpenGpxTracker/GPXScaleBar.swift")
VIEW_CONTROLLER = Path("/app/OpenGpxTracker/ViewController.swift")

# Regex that matches scaleBar.color / scaleBar?.forcedColor etc.
# Handles optional chaining (scaleBar?.) in addition to direct access (scaleBar.)
_SCALEBAR_COLOR_RE = r'scaleBar\??\.(\w*[Cc]olor)'


def test_scalebar_has_color_api():
    """GPXScaleBar must expose a way to set its color externally.

    The base code has NO API for color — it uses hardcoded system colors.
    Any correct fix must add a func or var involving UIColor so the
    ViewController can tell the scale bar what color to use.

    Accepted patterns (public keyword is optional — same-module access
    in Swift does not require it):
      - var <name>: UIColor            (any var typed as UIColor)
      - var <name>Color<...>: UIColor  (var with 'color' in the name)
      - func <name>Color<...>(         (func with 'color' in the name)
      - public func ...(UIColor)       (explicit public func taking UIColor)
    """
    content = SCALE_BAR.read_text()
    # public or internal func accepting UIColor
    has_func_with_uicolor = bool(re.search(
        r'func\s+\w+\s*\([^)]*UIColor[^)]*\)', content))
    # public or internal var typed as UIColor (with or without Optional ?)
    has_var_uicolor = bool(re.search(
        r'var\s+\w+\s*:\s*UIColor', content))
    # func with 'color' in its name
    has_func_with_color = bool(re.search(
        r'func\s+\w*[Cc]olor\w*\s*\(', content))
    assert has_func_with_uicolor or has_var_uicolor or has_func_with_color, \
        "GPXScaleBar should have a method or property to set its color"


def test_viewcontroller_sets_scalebar_color():
    """ViewController must set the scale bar's color as part of its
    tile-server color adaptation logic.

    The base code adjusts label colors but never touches the scale bar.
    Any correct fix must connect the tile server info to the scale bar.
    """
    content = VIEW_CONTROLLER.read_text()
    assert re.search(_SCALEBAR_COLOR_RE, content), \
        "ViewController should set a color-related property/method on the scale bar"


def test_scalebar_gets_white_for_dark_tiles():
    """Apple Satellite has dark imagery — the scale bar should be white.

    Verifies that .white appears in the context of the scale bar color
    operation, meaning the fix assigns white when the tile server is dark.
    """
    content = VIEW_CONTROLLER.read_text()
    # Find where scaleBar color is set, then check .white is nearby
    # (within the same function body — up to 800 chars in either direction)
    matches = list(re.finditer(_SCALEBAR_COLOR_RE, content))
    assert matches, "Should set a color on the scale bar"
    found = False
    for m in matches:
        window = content[max(0, m.start() - 800):m.end() + 800]
        if '.white' in window:
            found = True
            break
    assert found, \
        "Scale bar color logic should include .white (for dark-themed tiles like satellite)"


def test_scalebar_gets_black_for_light_tiles():
    """OpenStreetMap and similar tiles have light imagery — the scale bar
    should be black.

    Verifies that .black appears in the context of the scale bar color
    operation, meaning the fix assigns black when the tile server is light.
    """
    content = VIEW_CONTROLLER.read_text()
    matches = list(re.finditer(_SCALEBAR_COLOR_RE, content))
    assert matches, "Should set a color on the scale bar"
    found = False
    for m in matches:
        window = content[max(0, m.start() - 800):m.end() + 800]
        if '.black' in window:
            found = True
            break
    assert found, \
        "Scale bar color logic should include .black (for light-themed tiles like OSM)"
