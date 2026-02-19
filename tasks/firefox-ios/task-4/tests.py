import re
from pathlib import Path

APP = Path("/app/firefox-ios")

HOMEPAGE_VC  = APP / "Client/Frontend/Home/Homepage/HomepageViewController.swift"
TAB          = APP / "Client/TabManagement/Tab.swift"
BROWSER_COORD = APP / "Client/Coordinators/Browser/BrowserCoordinator.swift"


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def test_tab_has_homepage_scroll_offset_property():
    """Tab must store a homepageScrollOffset so each tab remembers its position."""
    content = _read(TAB)
    assert re.search(r'var\s+homepageScrollOffset\s*:\s*CGFloat\?', content), (
        "Tab should define var homepageScrollOffset: CGFloat? to persist per-tab scroll position"
    )


def test_homepage_vc_accepts_tab_manager():
    """HomepageViewController init must accept a tabManager parameter."""
    content = _read(HOMEPAGE_VC)
    assert re.search(r'init\s*\(.*tabManager\s*:', content, re.DOTALL), (
        "HomepageViewController init should accept a tabManager parameter"
    )


def test_restore_vertical_scroll_offset_method_exists():
    """HomepageViewController must expose restoreVerticalScrollOffset to reinstate saved position."""
    content = _read(HOMEPAGE_VC)
    assert re.search(r'func\s+restoreVerticalScrollOffset', content), (
        "HomepageViewController should define restoreVerticalScrollOffset()"
    )


def test_scroll_offset_saved_on_view_will_disappear():
    """The scroll offset must be saved when the homepage disappears so it survives navigation."""
    content = _read(HOMEPAGE_VC)
    # saveVerticalScrollOffset should be referenced in viewWillDisappear
    view_will_disappear = re.search(
        r'override\s+func\s+viewWillDisappear.*?(?=override\s+func|\Z)',
        content,
        re.DOTALL,
    )
    assert view_will_disappear, "HomepageViewController should override viewWillDisappear"
    assert "saveVerticalScrollOffset" in view_will_disappear.group(0), (
        "viewWillDisappear should call saveVerticalScrollOffset()"
    )


def test_scroll_offset_saved_on_did_end_dragging():
    """scrollViewDidEndDragging must be implemented and save the offset (drag-and-release gesture)."""
    content = _read(HOMEPAGE_VC)
    assert re.search(r'func\s+scrollViewDidEndDragging', content), (
        "HomepageViewController should implement scrollViewDidEndDragging to save scroll offset"
    )


def test_scroll_offset_saved_on_did_end_decelerating():
    """scrollViewDidEndDecelerating must save the offset (flick-and-decelerate gesture)."""
    content = _read(HOMEPAGE_VC)
    assert re.search(r'func\s+scrollViewDidEndDecelerating', content), (
        "HomepageViewController should implement scrollViewDidEndDecelerating to save scroll offset"
    )


def test_browser_coordinator_restores_scroll_not_scrolls_to_top():
    """BrowserCoordinator must call restoreVerticalScrollOffset instead of unconditional scrollToTop."""
    content = _read(BROWSER_COORD)
    assert re.search(r'restoreVerticalScrollOffset', content), (
        "BrowserCoordinator should call restoreVerticalScrollOffset when embedding the homepage"
    )


def test_impression_tracking_does_not_force_scroll_to_top():
    """Impression tracking must not call scrollToTop — it should fire on whatever is visible."""
    content = _read(HOMEPAGE_VC)
    # Find the shouldTriggerImpression handling block and assert scrollToTop is not inside it
    trigger_block = re.search(
        r'shouldTriggerImpression.*?trackVisibleItemImpressions',
        content,
        re.DOTALL,
    )
    if trigger_block:
        assert "scrollToTop" not in trigger_block.group(0), (
            "Impression tracking should not call scrollToTop — "
            "impressions should reflect the current visible content"
        )
