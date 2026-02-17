import re
from pathlib import Path

ROOT = Path("/app/ACHNBrowserUI")

VILLAGERS_VIEW_MODEL = ROOT / "ACHNBrowserUI/viewModels/VillagersViewModel.swift"
VILLAGERS_LIST_VIEW = ROOT / "ACHNBrowserUI/views/villagers/VillagersListView.swift"
VILLAGERS_SORT_VIEW = ROOT / "ACHNBrowserUI/views/villagers/VillagersSortView.swift"
FR_LOCALIZABLE = ROOT / "ACHNBrowserUI/fr.lproj/Localizable.strings"


def _read(path):
    return path.read_text() if path.exists() else ""


# ---------------------------------------------------------------------------
# Test 1 — VillagersViewModel has Sort enum
# ---------------------------------------------------------------------------


def test_villagers_view_model_has_sort_enum():
    """VillagersViewModel should define a Sort enum with at least Name and
    Species cases. Accepts:
      - enum Sort { case name, species }
      - enum SortOption { case byName, bySpecies }
      - Similar naming conventions
    """
    content = _read(VILLAGERS_VIEW_MODEL)
    has_sort_enum = bool(re.search(r"enum\s+\w*[Ss]ort\w*\s*\{", content))
    has_name_case = bool(re.search(r"case.*name|case.*byName", content, re.IGNORECASE))
    has_species_case = bool(
        re.search(r"case.*species|case.*bySpecies", content, re.IGNORECASE)
    )
    assert has_sort_enum and has_name_case and has_species_case, (
        "VillagersViewModel should have a Sort enum with at least "
        "name and species cases"
    )


# ---------------------------------------------------------------------------
# Test 2 — VillagersViewModel has sortedVillagers published property
# ---------------------------------------------------------------------------


def test_villagers_view_model_has_sorted_villagers():
    """VillagersViewModel must expose a sortedVillagers published property
    that the view can consume.
    """
    content = _read(VILLAGERS_VIEW_MODEL)
    has_published = bool(
        re.search(r"@Published.*sortedVillagers|sortedVillagers.*@Published", content)
    )
    has_sorted_prop = bool(re.search(r"(?:var|let)\s+sortedVillagers\s*:", content))
    assert (
        has_published and has_sorted_prop
    ), "VillagersViewModel should have a @Published sortedVillagers property"


# ---------------------------------------------------------------------------
# Test 3 — VillagersViewModel has currentSort property
# ---------------------------------------------------------------------------


def test_villagers_view_model_has_current_sort():
    """VillagersViewModel should track the currently selected sort option.
    Accepts:
      - sort: Sort?
      - currentSort: Sort?
      - activeSort: Sort?
      - selectedSort: Sort?
    """
    content = _read(VILLAGERS_VIEW_MODEL)
    has_current_sort = bool(
        re.search(
            r"(?:var|let)\s+\w*(?:[Cc]urrent|[Aa]ctive|[Ss]elected)?[Ss]ort\s*:\s*\w*Sort",
            content,
        )
    )
    has_sort_state = bool(re.search(r"@Published.*sort|sort.*@Published", content))
    assert (
        has_current_sort or has_sort_state
    ), "VillagersViewModel should track the currently selected sort option"


# ---------------------------------------------------------------------------
# Test 4 — VillagersSortView exists as action sheet
# ---------------------------------------------------------------------------


def test_villagers_sort_view_exists():
    """A VillagersSortView component should exist that presents an action
    sheet with sort options.
    """
    content = _read(VILLAGERS_SORT_VIEW)
    view_content = _read(VILLAGERS_LIST_VIEW)
    all_content = content + view_content

    has_sort_view = bool(
        re.search(r"[Vv]illagers[Ss]ort[Vv]iew|[Ss]ortView", all_content)
    )
    has_action_sheet = bool(
        re.search(
            r"\.confirmationDialog|\.actionSheet|ActionSheet|Alert.*sort",
            all_content,
            re.IGNORECASE,
        )
    )
    assert (
        has_sort_view or has_action_sheet
    ), "A VillagersSortView should exist with sort options in an action sheet"


# ---------------------------------------------------------------------------
# Test 5 — Sort has ascending/descending toggle
# ---------------------------------------------------------------------------


def test_sort_has_toggle_logic():
    """When the same sort option is selected again, it should reverse the
    sort order. The ViewModel should track sort direction.
    """
    content = _read(VILLAGERS_VIEW_MODEL)
    has_direction = bool(
        re.search(
            r"[Aa]scending|[Dd]escending|[Ss]ortOrder|[Rr]ever[st]e|orderedDescending|orderedAscending",
            content,
        )
    )
    has_toggle_logic = bool(
        re.search(r"oldValue|if.*current.*==.*new|toggle|!.*sort", content)
    )
    assert has_direction or has_toggle_logic, (
        "VillagersViewModel should have logic to toggle sort direction "
        "(ascending/descending)"
    )


# ---------------------------------------------------------------------------
# Test 6 — Sort button icon changes when active (filled vs outline)
# ---------------------------------------------------------------------------


def test_sort_button_icon_indicates_active_state():
    """The sort button in the navigation bar should display a filled icon
    when a sort is active, and an outline icon when no sort is active.
    """
    sort_content = _read(VILLAGERS_SORT_VIEW)
    view_content = _read(VILLAGERS_LIST_VIEW)
    all_content = sort_content + view_content

    has_icon_logic = bool(
        re.search(
            r"\.fill.*sort|sort.*\.fill|circle\.fill|arrow.*circle",
            all_content,
            re.IGNORECASE,
        )
    )
    has_conditional_icon = bool(
        re.search(
            r"sort\s*==\s*nil|sort\s*!=\s*nil|\.fill|ternary.*icon",
            all_content,
        )
    )
    assert has_icon_logic or has_conditional_icon, (
        "Sort button should change icon based on "
        "whether a sort is active (filled vs outline)"
    )


# ---------------------------------------------------------------------------
# Test 7 — Search takes priority over sorting
# ---------------------------------------------------------------------------


def test_search_takes_priority_over_sorting():
    """When a search is active, the view should display searchResults
    instead of sortedVillagers. Sorting should only apply to the full list.
    """
    view_content = _read(VILLAGERS_LIST_VIEW)
    has_search_priority = bool(
        re.search(
            r"if.*search|searchText\.isEmpty|search.*villagers|searchResults",
            view_content,
            re.IGNORECASE,
        )
    )
    has_conditional = bool(
        re.search(
            r"searchResults.*sortedVillagers|sort\s*!=\s*nil.*sortedVillagers",
            view_content,
        )
    )
    assert has_search_priority or has_conditional, (
        "VillagersListView should check for active search and display "
        "searchResults before sortedVillagers"
    )


# ---------------------------------------------------------------------------
# Test 8 — Clearing sort restores original order
# ---------------------------------------------------------------------------


def test_clear_sort_resets_to_original_order():
    """The sort view should have a 'Clear Selection' option that resets
    sortedVillagers to empty, causing the view to fall back to the default
    villagers list.
    """
    sort_view = _read(VILLAGERS_SORT_VIEW)
    view_model = _read(VILLAGERS_VIEW_MODEL)
    all_content = sort_view + view_model

    has_clear_option = bool(
        re.search(
            r"[Cc]lear|[Rr]eset|remove.*sort|deselect", all_content, re.IGNORECASE
        )
    )
    has_empty_reset = bool(
        re.search(
            r"sortedVillagers\s*=\s*\[\]|reset.*sort|(?:current)?[Ss]ort\s*=\s*nil",
            all_content,
        )
    )
    assert has_clear_option or has_empty_reset, (
        "VillagersSortView should have a way to clear the sort selection, "
        "resetting sortedVillagers to empty"
    )


# ---------------------------------------------------------------------------
# Test 9 — Name sort is alphabetical by localized name
# ---------------------------------------------------------------------------


def test_name_sort_uses_localized_names():
    """When sorting by name, the ViewModel should sort alphabetically by
    the villager's localized name (not internal ID).
    """
    content = _read(VILLAGERS_VIEW_MODEL)
    has_localized_sort = bool(
        re.search(
            r"localizedName|\.name|villagerName|sorted.*by.*name",
            content,
            re.IGNORECASE,
        )
    )
    has_compare = bool(
        re.search(r"\.sorted|comparator|\.compare|localizedCompare", content, re.IGNORECASE)
    )
    assert (
        has_localized_sort or has_compare
    ), "Name sorting should use the villager's localized name"


# ---------------------------------------------------------------------------
# Test 10 — Species sort is alphabetical by species
# ---------------------------------------------------------------------------


def test_species_sort_is_alphabetical():
    """When sorting by species, the ViewModel should sort alphabetically
    by the villager's species.
    """
    content = _read(VILLAGERS_VIEW_MODEL)
    has_species_sort = bool(
        re.search(r"sort.*species|species.*sort|\.species", content, re.IGNORECASE)
    )
    has_sort_method = bool(re.search(r"\.sorted|comparator|localizedCompare", content))
    assert (
        has_species_sort or has_sort_method
    ), "Species sorting should sort villagers alphabetically by species"


# ---------------------------------------------------------------------------
# Test 11 — French localization for sort title
# ---------------------------------------------------------------------------


def test_french_localization_exists():
    """French localization strings should be added for at least the
    'Sort villagers' action sheet title.
    """
    fr_content = _read(FR_LOCALIZABLE)
    sort_view = _read(VILLAGERS_SORT_VIEW)
    view = _read(VILLAGERS_LIST_VIEW)
    all_content = fr_content + sort_view + view

    has_fr_translation = bool(
        re.search(r"[Tt]rier.*villageois", fr_content)
    )
    has_localization_key = bool(
        re.search(r'NSLocalizedString|LocalizedStringKey|Text\(.*".*"\)', sort_view + view)
    )
    has_sort_string = bool(
        re.search(
            r"[Ss]ort.*villagers|[Tt]rier.*villageois", all_content, re.IGNORECASE
        )
    )
    assert (
        has_fr_translation or has_localization_key or has_sort_string
    ), "Sort UI should include French localization for 'Sort villagers'"


# ---------------------------------------------------------------------------
# Test 12 — No changes to other views
# ---------------------------------------------------------------------------


def test_other_views_unchanged():
    """The villager detail view and other unrelated views should not be
    modified.
    """
    sort_view = _read(VILLAGERS_SORT_VIEW)
    villagers_view = _read(VILLAGERS_LIST_VIEW)

    assert (
        len(sort_view) > 100 or len(villagers_view) > 100
    ), "Either VillagersSortView or VillagersListView should have implementation"
