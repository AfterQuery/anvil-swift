import re
from pathlib import Path

APP = Path("/app/firefox-ios")

FEATURE_FLAGS  = APP / "Client/FeatureFlags/LegacyFeatureFlagsManager.swift"
DATA_SOURCE    = APP / "Client/Frontend/Home/Homepage/HomepageDiffableDataSource.swift"
HOMEPAGE_VC    = APP / "Client/Frontend/Home/Homepage/HomepageViewController.swift"
CACHE          = APP / "Client/Frontend/Home/Homepage/Layout/HomepageLayoutMeasurementCache.swift"
LAYOUT         = APP / "Client/Frontend/Home/Homepage/Layout/HomepageSectionLayoutProvider.swift"
STORY_PROVIDER = APP / "Client/Frontend/Home/Homepage/Merino/StoryProvider.swift"


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def test_stories_scroll_direction_customized_property_exists():
    """LegacyFeatureFlagsManager must expose isHomepageStoriesScrollDirectionCustomized."""
    content = _read(FEATURE_FLAGS)
    assert re.search(r'var\s+isHomepageStoriesScrollDirectionCustomized', content), (
        "LegacyFeatureFlagsManager should define isHomepageStoriesScrollDirectionCustomized"
    )


def test_stories_scroll_direction_checks_phone_idiom():
    """The customized-scroll-direction guard must restrict to iPhone (not iPad)."""
    content = _read(FEATURE_FLAGS)
    assert re.search(r'userInterfaceIdiom\s*==\s*\.phone', content), (
        "isHomepageStoriesScrollDirectionCustomized should check for .phone userInterfaceIdiom"
    )


def test_stories_feed_cell_registered_in_datasource():
    """HomepageDiffableDataSource must register StoriesFeedCell for dequeue."""
    content = _read(DATA_SOURCE)
    assert "StoriesFeedCell" in content, (
        "HomepageDiffableDataSource should register StoriesFeedCell"
    )


def test_scroll_to_top_uses_adjusted_content_inset():
    """scrollToTop must account for adjustedContentInset to avoid incorrect offset."""
    content = _read(HOMEPAGE_VC)
    assert re.search(r'adjustedContentInset', content), (
        "scrollToTop should use adjustedContentInset to correctly scroll to top"
    )
    assert not re.search(r'setContentOffset\s*\(\s*\.zero', content), (
        "scrollToTop should not use .zero as the content offset"
    )


def test_vertical_stories_layout_method_exists():
    """HomepageSectionLayoutProvider must have a dedicated vertical stories layout method."""
    content = _read(LAYOUT)
    assert re.search(r'func\s+create\w*[Vv]ertical\w*Layout', content), (
        "HomepageSectionLayoutProvider should define a vertical stories section layout method"
    )


def test_vertical_layout_uses_fractional_width():
    """Vertical stories items must be full-width (fractionalWidth 1.0), not a fixed card size."""
    content = _read(LAYOUT)
    assert re.search(r'fractionalWidth\s*\(\s*1\.0\s*\)', content), (
        "Vertical stories layout should use fractionalWidth(1.0) for full-width cells"
    )


def test_scroll_direction_included_in_measurement_cache_key():
    """The stories measurement cache key must include scrollDirection to avoid stale layouts."""
    content = _read(CACHE)
    assert re.search(r'scrollDirection\s*:', content), (
        "StoriesMeasurement.Key should include scrollDirection to prevent stale layout reuse"
    )


def test_story_provider_fetches_more_stories_when_customized():
    """StoryProvider must fetch up to 100 stories when the scroll direction is customized."""
    content = _read(STORY_PROVIDER)
    assert re.search(r'100', content), (
        "StoryProvider should fetch up to 100 stories for customized scroll direction"
    )
    assert re.search(r'isHomepageStoriesScrollDirectionCustomized', content), (
        "StoryProvider should check isHomepageStoriesScrollDirectionCustomized to decide story count"
    )
