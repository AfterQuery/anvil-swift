import re
from pathlib import Path

ROOT = Path("/app/ACHNBrowserUI")

ITEM = ROOT / "ACHNBrowserUI/packages/Backend/Sources/Backend/models/Item.swift"
VIEW_MODEL = ROOT / "ACHNBrowserUI/viewModels/ActiveCrittersViewModel.swift"
VIEW = ROOT / "ACHNBrowserUI/views/critters/ActiveCrittersView.swift"


def _read(path):
    return path.read_text() if path.exists() else ""


# ---------------------------------------------------------------------------
# Test 1 — Item must have hour-level activity checking
# ---------------------------------------------------------------------------

def test_item_has_hour_level_check():
    """Item must expose a way to check if a critter is active at the current
    hour/time.  The base code only checks the month (isActive), not the hour.

    Accepts:
      - A new method with hour/now/time in the name (isActiveNow, isActiveAtThisHour, etc.)
      - An isActive overload that takes a Date or hour parameter
    """
    content = _read(ITEM)
    has_hour_func = bool(re.search(
        r'func\s+\w*(?:[Aa]ctive|[Aa]vailable|[Cc]atch)\w*(?:[Hh]our|[Nn]ow|[Tt]ime)\w*\s*\(.*\)\s*->\s*Bool',
        content))
    has_active_date_overload = bool(re.search(
        r'func\s+isActive\s*\(.*(?:[Dd]ate|[Hh]our)',
        content))
    assert has_hour_func or has_active_date_overload, (
        "Item should have a Bool-returning method to check if a critter is "
        "active at the current hour (e.g. isActiveAtThisHour() -> Bool, "
        "or isActive(at date: Date) -> Bool)"
    )


# ---------------------------------------------------------------------------
# Test 2 — ViewModel provides two separate catch collections
# ---------------------------------------------------------------------------

def test_view_model_has_two_catch_collections():
    """The ViewModel must split the single toCatch into two separate
    collections — one for critters catchable now and one for later.

    Accepts any naming convention: toCatchNow/toCatchLater,
    catchNow/catchLater, availableNow/availableLater, etc.
    """
    content = _read(VIEW_MODEL)
    # Look for two distinct properties with "now" and "later" (or similar)
    has_now = bool(re.search(r'(?:catch|available|active)\w*[Nn]ow', content, re.IGNORECASE))
    has_later = bool(re.search(r'(?:catch|available|active)\w*[Ll]ater', content, re.IGNORECASE))
    assert has_now and has_later, (
        "ViewModel should have two separate catch collections "
        "(e.g. toCatchNow/toCatchLater) instead of a single toCatch"
    )


# ---------------------------------------------------------------------------
# Test 3 — ViewModel no longer has a single toCatch property
# ---------------------------------------------------------------------------

def test_view_model_single_to_catch_removed():
    """The old single `toCatch` property (without Now/Later distinction)
    should no longer be the only catch collection in the ViewModel.
    """
    content = _read(VIEW_MODEL)
    # The old code has `let toCatch: [Item]` and `let toCatch = active.filter{...}`
    # After the patch, these become toCatchNow/toCatchLater
    single_decl = re.findall(r'\btoCatch\b(?!Now|Later|now|later)', content)
    has_split = bool(re.search(r'(?:catch|available|active)\w*[Nn]ow', content, re.IGNORECASE))
    assert has_split or len(single_decl) == 0, (
        "The single toCatch should be split into now/later collections"
    )


# ---------------------------------------------------------------------------
# Test 4 — View shows "To catch now" section
# ---------------------------------------------------------------------------

def test_view_has_catch_now_section():
    """ActiveCrittersView must display a section for critters catchable now.
    """
    content = _read(VIEW)
    has_now = bool(re.search(
        r'["\']To\s+catch\s+now["\']', content, re.IGNORECASE))
    assert has_now, (
        "ActiveCrittersView should have a 'To catch now' section"
    )


# ---------------------------------------------------------------------------
# Test 5 — View shows "To catch later" section
# ---------------------------------------------------------------------------

def test_view_has_catch_later_section():
    """ActiveCrittersView must display a section for critters catchable later.
    """
    content = _read(VIEW)
    has_later = bool(re.search(
        r'["\']To\s+catch\s+later["\']', content, re.IGNORECASE))
    assert has_later, (
        "ActiveCrittersView should have a 'To catch later' section"
    )


# ---------------------------------------------------------------------------
# Test 6 — Old single "To catch" section is removed from the view
# ---------------------------------------------------------------------------

def test_old_to_catch_section_removed():
    """The old single 'To catch' section (without 'now' or 'later') should
    no longer appear in ActiveCrittersView.
    """
    content = _read(VIEW)
    # Match exact "To catch" but NOT "To catch now" or "To catch later"
    old_matches = re.findall(r'["\']To catch["\']', content)
    assert len(old_matches) == 0, (
        "The old 'To catch' section should be replaced with "
        "'To catch now' and 'To catch later'"
    )
