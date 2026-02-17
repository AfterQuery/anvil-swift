#!/bin/bash
set -e

cd /app

# Create test directory preserving original structure
mkdir -p tasks/task-1

cat > tasks/task-1/task_tests.py << 'ANVIL_TEST_CODE'
import re
from pathlib import Path

ROOT = Path("/app/OpenGpxTracker")

SCALE_BAR = ROOT / "GPXScaleBar.swift"
VIEW_CONTROLLER = ROOT / "ViewController.swift"
MAP_VIEW = ROOT / "GPXMapView.swift"


def _read(path):
    return path.read_text() if path.exists() else ""


# ---------------------------------------------------------------------------
# Test 1 — GPXScaleBar must have a NEW appearance control API
# ---------------------------------------------------------------------------

def test_scalebar_has_appearance_api():
    """GPXScaleBar must expose a way to control its appearance.

    The base code has NO such API — colors are hardcoded to system colors.
    Accepts any of:
      - A var typed as UIColor (e.g. forcedColor: UIColor?)
      - A func accepting UIColor
      - A func/var with 'color' in the name
      - A Bool var for dark/light (e.g. isDarkBackground: Bool)
    """
    content = _read(SCALE_BAR)

    # func accepting UIColor
    has_func_uicolor = bool(re.search(
        r'func\s+\w+\s*\([^)]*UIColor[^)]*\)', content))
    # var typed as UIColor
    has_var_uicolor = bool(re.search(
        r'var\s+\w+\s*:\s*UIColor', content))
    # func with 'color' in name
    has_color_func = bool(re.search(
        r'func\s+\w*[Cc]olor\w*\s*\(', content))
    # var with 'color' in name
    has_color_var = bool(re.search(
        r'var\s+\w*[Cc]olor\w*\s*:', content))
    # Bool property for dark/light (e.g. isDarkBackground, isDark)
    has_dark_bool = bool(re.search(
        r'var\s+\w*[Dd]ark\w*\s*:\s*Bool', content))

    assert (
        has_func_uicolor or has_var_uicolor or has_color_func
        or has_color_var or has_dark_bool
    ), "GPXScaleBar should have a method or property to control its appearance"


# ---------------------------------------------------------------------------
# Test 2 — The tile server must influence the scale bar
# ---------------------------------------------------------------------------

def test_tile_server_influences_scalebar():
    """The tile server must influence the scale bar's appearance.

    The connection can live in ViewController, GPXMapView, or even
    GPXScaleBar itself (self-updating via notification / mapView query).
    """
    # Check ViewController and GPXMapView for scaleBar property access
    # near tile-server-related context
    scalebar_prop_re = r'scaleBar\??\.\w+'
    tile_context_re = r'tileServer|isDark|colorMode|hasDark|needForce|forcedColor'

    for path in (VIEW_CONTROLLER, MAP_VIEW):
        content = _read(path)
        for m in re.finditer(scalebar_prop_re, content):
            window = content[max(0, m.start() - 600):m.end() + 600]
            if re.search(tile_context_re, window, re.IGNORECASE):
                return

    # Also accept GPXScaleBar internally querying its mapView for tile info
    sb = _read(SCALE_BAR)
    if re.search(r'tileServer|isDark\w*Map', sb):
        return

    assert False, "Tile server should influence the scale bar appearance"


# ---------------------------------------------------------------------------
# Test 3 — White for dark tiles (e.g. satellite)
# ---------------------------------------------------------------------------

def test_scalebar_gets_white_for_dark_tiles():
    """Apple Satellite has dark imagery — the scale bar should be white.

    Checks that .white appears in GPXScaleBar's color logic (internal
    approach), OR near a scaleBar property access in ViewController/
    GPXMapView (external approach).

    NOTE: .white already exists in the base ViewController for label
    colors, so we must check in context — not just grep the whole file.
    """
    # Pattern A: .white in GPXScaleBar.swift (NOT present in base code)
    sb = _read(SCALE_BAR)
    if '.white' in sb:
        return

    # Pattern B: .white near a scaleBar property access in VC / MapView
    for path in (VIEW_CONTROLLER, MAP_VIEW):
        content = _read(path)
        for m in re.finditer(r'scaleBar\??\.\w+', content):
            window = content[max(0, m.start() - 800):m.end() + 800]
            if '.white' in window:
                return

    assert False, \
        "Scale bar color logic should include .white (for dark-themed tiles like satellite)"


# ---------------------------------------------------------------------------
# Test 4 — Black for light tiles (e.g. OSM)
# ---------------------------------------------------------------------------

def test_scalebar_gets_black_for_light_tiles():
    """OpenStreetMap and similar tiles have light imagery — the scale bar
    should be black.

    Checks that .black appears alongside .white in GPXScaleBar (colour
    differentiation — the base only has .black as a pre-iOS 13 fallback),
    OR near a scaleBar property access in ViewController/GPXMapView.
    """
    # Pattern A: both .white AND .black in GPXScaleBar
    # (base code has .black but NOT .white — requiring both ensures the
    #  color logic was actually added, not just the old fallback)
    sb = _read(SCALE_BAR)
    if '.white' in sb and '.black' in sb:
        return

    # Pattern B: .black near a scaleBar property access in VC / MapView
    for path in (VIEW_CONTROLLER, MAP_VIEW):
        content = _read(path)
        for m in re.finditer(r'scaleBar\??\.\w+', content):
            window = content[max(0, m.start() - 800):m.end() + 800]
            if '.black' in window:
                return

    assert False, \
        "Scale bar color logic should include .black (for light-themed tiles like OSM)"

ANVIL_TEST_CODE

python3 -m pytest -v tasks/task-1/task_tests.py 2>&1 || true
