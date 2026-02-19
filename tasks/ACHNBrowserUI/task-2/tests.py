import re
from pathlib import Path

ROOT = Path("/app/ACHNBrowserUI")

TURNIPS_VIEW = ROOT / "ACHNBrowserUI/views/turnips/TurnipsView.swift"
TURNIPS_DIR = ROOT / "ACHNBrowserUI/views/turnips"
ROWS_DIR = ROOT / "ACHNBrowserUI/views/turnips/rows"


def _read(path):
    return path.read_text() if path.exists() else ""


def _read_all_swift_in_dir(directory):
    """Read all .swift files in a directory (non-recursive)."""
    if not directory.exists():
        return ""
    return "\n".join(f.read_text() for f in sorted(directory.glob("*.swift")) if f.is_file())


# ---------------------------------------------------------------------------
# Test 1 — TurnipsView uses a grid-based layout
# ---------------------------------------------------------------------------

def test_turnips_view_uses_grid_layout():
    """The turnip price table must use a grid-based layout component
    (GridStack, LazyVGrid, Grid, or similar) instead of plain HStack rows.
    Checks all swift files in the turnips directory.
    """
    content = _read_all_swift_in_dir(TURNIPS_DIR)
    has_grid = bool(re.search(
        r'GridStack|LazyVGrid|LazyHGrid|\bGrid\b(?!\w)', content))
    has_fixed_width_columns = bool(re.search(
        r'\.frame\(.*width\s*:.*\).*\.frame\(.*width\s*:', content, re.DOTALL))
    assert has_grid or has_fixed_width_columns, (
        "Turnips views should use a grid layout component "
        "(e.g. GridStack, LazyVGrid, Grid) or fixed-width frame columns for the price table"
    )


# ---------------------------------------------------------------------------
# Test 2 — Old separate row views are removed
# ---------------------------------------------------------------------------

def test_old_row_views_removed():
    """The old separate row view files that caused misalignment should be
    removed or consolidated. The base code has TurnipsAveragePriceRow.swift,
    TurnipsMinMaxPriceRow.swift, and TurnipsPriceRow.swift in a rows/ dir.
    """
    old_files = [
        ROWS_DIR / "TurnipsAveragePriceRow.swift",
        ROWS_DIR / "TurnipsMinMaxPriceRow.swift",
        ROWS_DIR / "TurnipsPriceRow.swift",
    ]
    still_exist = [f.name for f in old_files if f.exists()]
    assert len(still_exist) == 0, (
        f"Old row view files should be removed (still found: {still_exist}). "
        "The grid layout should replace these separate row views."
    )


# ---------------------------------------------------------------------------
# Test 3 — TurnipsView no longer uses the old row views
# ---------------------------------------------------------------------------

def test_old_row_references_removed():
    """TurnipsView should no longer reference the old row structs
    (TurnipsAveragePriceRow, TurnipsMinMaxPriceRow) that caused alignment
    issues with their individual HStack layouts.
    """
    content = _read(TURNIPS_VIEW)
    has_avg_row = bool(re.search(r'TurnipsAveragePriceRow', content))
    has_minmax_row = bool(re.search(r'TurnipsMinMaxPriceRow', content))
    assert not has_avg_row and not has_minmax_row, (
        "TurnipsView should not reference old row structs "
        "(TurnipsAveragePriceRow, TurnipsMinMaxPriceRow)"
    )


# ---------------------------------------------------------------------------
# Test 4 — Price data rendered with column-based logic
# ---------------------------------------------------------------------------

def test_column_based_rendering():
    """The price display must use column-based rendering (e.g. a function
    taking row/column indices, or a column switch) rather than the old
    approach of one HStack per row with Spacers between values.
    Checks all swift files in the turnips directory.
    """
    content = _read_all_swift_in_dir(TURNIPS_DIR)
    has_row_col = bool(re.search(r'row.*column|column.*row', content))
    has_col_switch = bool(re.search(r'switch\s+column', content))
    has_grid_items = bool(re.search(r'GridItem|columns\s*:', content))
    has_aligned_columns = bool(re.search(
        r'\.frame\(.*[Ww]idth\s*:.*alignment\s*:', content))
    assert has_row_col or has_col_switch or has_grid_items or has_aligned_columns, (
        "Price values should be rendered using column-based logic "
        "(row/column indices, column switch, GridItem columns, or fixed-width aligned frames)"
    )


# ---------------------------------------------------------------------------
# Test 5 — Grid used for all three display modes
# ---------------------------------------------------------------------------

def test_grid_used_for_all_display_modes():
    """The grid layout must be used for all three turnip display modes:
    average prices, min/max prices, and profits. The base code uses
    separate ForEach+row patterns for each.
    Checks all swift files in the turnips directory.
    """
    content = _read_all_swift_in_dir(TURNIPS_DIR)
    grid_usages = len(re.findall(
        r'GridStack|LazyVGrid|LazyHGrid|\bGrid\s*\(', content))
    has_unified_component = bool(re.search(
        r'enum\s+\w*(?:[Dd]isplay[Mm]ode|[Pp]redictions?[Dd]isplay|[Pp]rice[Mm]ode)\w*'
        r'|[Pp]rice[Gg]rid|[Tt]urnips[Pp]rice[Gg]rid|[Tt]urnips[Pp]rices[Tt]able',
        content))
    has_geometry_columns = (
        len(re.findall(r'GeometryReader', content)) >= 1
        and len(re.findall(r'\.frame\(.*width\s*:', content)) >= 3
    )
    assert grid_usages >= 3 or has_unified_component or has_geometry_columns, (
        f"Expected grid layout to be used for all 3 display modes "
        f"(average, min/max, profits) via separate grid instances, a unified component "
        f"(e.g. DisplayMode enum, PriceGrid), or GeometryReader with fixed-width columns; "
        f"found {grid_usages} grid usage(s)"
    )


# ---------------------------------------------------------------------------
# Test 6 — eraseToAnyViewForRow helper removed
# ---------------------------------------------------------------------------

def test_erase_to_any_view_for_row_removed():
    """The eraseToAnyViewForRow() workaround (which wrapped rows in VStack)
    should no longer be needed — the grid handles row layout directly.
    """
    content = _read(TURNIPS_VIEW)
    view_ext = _read(ROOT / "ACHNBrowserUI/extensions/View.swift")
    combined = content + view_ext
    assert 'eraseToAnyViewForRow' not in combined, (
        "eraseToAnyViewForRow() should be removed — "
        "the grid layout handles row structure directly"
    )
