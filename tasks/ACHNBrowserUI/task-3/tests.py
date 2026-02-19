import re
from pathlib import Path

ROOT = Path("/app/ACHNBrowserUI")

USER_COLLECTION = ROOT / "Packages/Backend/Sources/Backend/Environments/UserCollection.swift"
BACKEND_MODELS_DIR = ROOT / "Packages/Backend/Sources/Backend/Models"
BACKEND_ENV_DIR = ROOT / "Packages/Backend/Sources/Backend/Environments"
ITEM = ROOT / "Packages/Backend/Sources/Backend/Models/Item.swift"
ITEM_DETAIL_VIEW = ROOT / "ACHNBrowserUI/views/items/detail/ItemDetailView.swift"
LIKE_BUTTON_VIEW = ROOT / "ACHNBrowserUI/views/shared/LikeButtonView.swift"
LIKE_BUTTON_VM = ROOT / "ACHNBrowserUI/viewModels/LikeButtonViewModel.swift"
VARIANTS_FOR_LIKE_VIEW = ROOT / "ACHNBrowserUI/views/shared/VariantsForLikeView.swift"
SHARED_VIEWS_DIR = ROOT / "ACHNBrowserUI/views/shared"
VIEW_MODELS_DIR = ROOT / "ACHNBrowserUI/viewModels"


def _read(path):
    return path.read_text() if path.exists() else ""


def _read_all_swift(directories):
    """Read all .swift files in multiple directories (non-recursive)."""
    contents = []
    for d in directories:
        if d.exists():
            contents.extend(f.read_text() for f in sorted(d.glob("*.swift")) if f.is_file())
    return "\n".join(contents)


# ---------------------------------------------------------------------------
# Test 1 — UserCollection tracks variant completion status
# ---------------------------------------------------------------------------


def test_user_collection_tracks_variant_completion():
    """UserCollection must have a way to determine the like status based on
    variant completion — returning a state like unstarted/partial/complete
    (or none/partial/complete).
    """
    all_content = _read_all_swift([BACKEND_MODELS_DIR, BACKEND_ENV_DIR, VIEW_MODELS_DIR])
    has_status_enum = bool(
        re.search(
            r"enum\s+\w*(?:[Cc]ompletion|[Cc]ollection|[Pp]rogress|[Ss]tat(?:us|e))\w*",
            all_content,
        )
    )
    has_partial_case = bool(
        re.search(
            r"case\s+(?:unstarted|none|partial|complete)",
            all_content,
        )
    )
    has_status_func = bool(
        re.search(
            r"func\s+\w*(?:[Cc]ompletion[Ss]tatus|[Cc]ollection[Ss]tate|[Pp]rogress[Ss]tate)\s*\(",
            all_content,
        )
    )
    assert (has_status_enum and has_partial_case) or has_status_func, (
        "A variant collection status enum should be defined "
        "(e.g. VariantsCompletionStatus, VariantCollectionState, ItemCollectionProgressState "
        "with cases like none/unstarted, partial, complete)"
    )


# ---------------------------------------------------------------------------
# Test 2 — Item model has variant information
# ---------------------------------------------------------------------------


def test_item_has_variant_properties():
    """There must be a way to check whether an item has multiple variants.
    Accepts: a computed Bool property (hasSomeVariations, hasMultipleVariants,
    hasVariants) on Item, UserCollection, or LikeButtonViewModel, or an
    inline check like `variations?.count > 1` / `variants.count > 1`.
    """
    all_content = _read_all_swift([BACKEND_MODELS_DIR, BACKEND_ENV_DIR, VIEW_MODELS_DIR, SHARED_VIEWS_DIR])

    has_variant_bool = bool(
        re.search(
            r"var\s+\w*(?:[Hh]as[Vv]ariant|[Hh]as[Ss]ome[Vv]ariation|[Hh]asMultiple[Vv]ariant)\w*\s*:\s*Bool",
            all_content,
        )
    )
    has_inline_check = bool(
        re.search(
            r"variant(?:ion)?s?\?*\.count\s*(?:>|>=)\s*[12]|variant(?:ion)?s?\?*\.count\s*.*>\s*1",
            all_content,
        )
    )
    assert has_variant_bool or has_inline_check, (
        "There should be a way to check if an item has multiple variants "
        "(e.g. hasSomeVariations: Bool, or variations?.count > 1)"
    )


# ---------------------------------------------------------------------------
# Test 3 — Half-star icon or partial state indicator exists
# ---------------------------------------------------------------------------


def test_partial_like_state_indicator_exists():
    """The UI must have a way to display partial like state (half-star icon).
    Accepts:
      - "leadinghalf" in icon/image name (star.leadinghalf.fill)
      - "half" in icon/image name
      - PartialStar or HalfStar view
      - .partial case in completion status
      - isPartial or partialCompletion variable
    """
    like_button_content = _read(LIKE_BUTTON_VIEW)
    like_vm_content = _read(LIKE_BUTTON_VM)
    item_detail_content = _read(ITEM_DETAIL_VIEW)
    all_content = like_button_content + like_vm_content + item_detail_content

    has_half_star = bool(
        re.search(
            r"leadinghalf|[Hh]alf[Ss]tar|[Pp]artial[Ss]tar|\.half\b", all_content
        )
    )
    has_partial_logic = bool(
        re.search(
            r"is[Pp]artial|[Pp]artial[Cc]ompletion|\.partial|completionStatus",
            all_content,
        )
    )
    assert has_half_star or has_partial_logic, (
        "LikeButtonView should have a half-star icon "
        "or partial state indicator"
    )


# ---------------------------------------------------------------------------
# Test 4 — Variant selection bottom sheet / overlay exists
# ---------------------------------------------------------------------------


def test_variant_selection_view_exists():
    """A view component should exist for selecting individual variants.
    Accepts:
      - VariantsForLikeView, VariantSelectionSheet, VariantBottomSheet
      - ".sheet" modifier with variant selection
      - VariantListView as a sheet/modal/overlay
    """
    sheet_content = _read(VARIANTS_FOR_LIKE_VIEW)
    like_button = _read(LIKE_BUTTON_VIEW)

    all_content = sheet_content + like_button

    has_variant_view = bool(
        re.search(
            r"[Vv]ariant[Ss](?:ForLike|election|Sheet|BottomSheet)|[Vv]ariant(?:[Ss]election)?[Ss]heet",
            all_content,
        )
    )
    has_modal = bool(
        re.search(r"\.sheet\(|\.fullScreenCover\(|\.modal\(|@State.*showVariant|@Binding.*item", all_content)
    )
    assert has_variant_view or has_modal, (
        "A variant selection view should exist "
        "(e.g. VariantsForLikeView, VariantSelectionSheet)"
    )


# ---------------------------------------------------------------------------
# Test 5 — ItemDetail favorite button triggers variant selection
# ---------------------------------------------------------------------------


def test_item_detail_favorite_button_shows_variants():
    """When an item with variants is tapped on the favorite button,
    it should show the variant selection view instead of just toggling
    the parent item. This logic can be in ItemDetailView or LikeButtonView.
    """
    content = _read(ITEM_DETAIL_VIEW)
    like_content = _read(LIKE_BUTTON_VIEW)
    vm_content = _read(LIKE_BUTTON_VM)
    all_content = content + like_content + vm_content

    has_variant_trigger = bool(
        re.search(
            r"itemToDisplayVariantsLike|likedItemWithVariants|showVariant|presentVariant|showingVariant|variantSelector|variantSheet",
            all_content,
            re.IGNORECASE,
        )
    )
    has_variation_check = bool(
        re.search(
            r"hasSomeVariations|hasVariants|hasMultipleVariants|variant.*sheet|VariantsForLike|VariantSelection|VariantSelector",
            all_content,
            re.IGNORECASE,
        )
    )
    assert has_variant_trigger or has_variation_check, (
        "ItemDetailView or LikeButtonView should trigger variant selection when "
        "favorite button is tapped for multi-variant items"
    )


# ---------------------------------------------------------------------------
# Test 6 — Parent item synced with variants (auto-add on first like)
# ---------------------------------------------------------------------------


def test_parent_item_synced_on_variant_like():
    """When the first variant of an item is liked, the parent item should
    automatically be added to the collection. This can be done by checking
    completion/collection/progress state after variant toggle, or by
    syncing the parent item based on collected variant count.
    """
    all_content = _read_all_swift([BACKEND_ENV_DIR, VIEW_MODELS_DIR])

    status_pattern = r"[Cc]ompletion[Ss]tatus|[Cc]ollection[Ss]tate|[Pp]rogress[Ss]tate"
    has_sync_in_toggle_variant = bool(
        re.search(
            r"(?:" + status_pattern + r").*toggleItem|toggleItem.*(?:" + status_pattern + r")",
            all_content, re.DOTALL,
        )
    )
    has_auto_add = bool(
        re.search(
            r"(?:" + status_pattern + r")\s*(?:!=|==)\s*\.(?:unstarted|none|complete)",
            all_content,
        )
    )
    has_collected_count_sync = bool(
        re.search(r"collected\s*==\s*0|variants\[.*\]\?*\.count\s*(?:==|>)\s*0", all_content)
    ) and bool(
        re.search(r"toggleItem|contains\(item\)|isInCollection", all_content)
    )
    assert has_sync_in_toggle_variant or has_auto_add or has_collected_count_sync, (
        "toggleVariant should auto-add/remove the parent item "
        "based on collection state (e.g. toggle when status changes to/from none/unstarted, "
        "or sync based on collected variant count)"
    )


# ---------------------------------------------------------------------------
# Test 7 — Items without variants don't use partial like system
# ---------------------------------------------------------------------------


def test_items_without_variants_unaffected():
    """Items with zero or one variant should not display the partial like
    system. Only items with 2+ variants should show half-star state.
    """
    all_content = _read_all_swift([BACKEND_ENV_DIR, BACKEND_MODELS_DIR, VIEW_MODELS_DIR, SHARED_VIEWS_DIR])

    has_variant_count_check = bool(
        re.search(
            r"variant(?:ion)?s?\?*\.count\s*[<>=>\s]|variant[Cc]ount\s*[<>=]|\bvariantCount\b",
            all_content,
        )
    )
    has_multi_variant_check = bool(
        re.search(
            r"variant(?:ion)?s?\?*\.count\s*.*[>]\s*1|hasSomeVariations|hasMultiple[Vv]ariants|hasVariants",
            all_content,
        )
    )
    assert has_variant_count_check or has_multi_variant_check, (
        "Should check if an item has multiple variants before using "
        "the partial like system"
    )


# ---------------------------------------------------------------------------
# Test 8 — Partial like status updates dynamically
# ---------------------------------------------------------------------------


def test_variant_selection_updates_like_state():
    """When variants are toggled in the variant selection view, the like
    icon should update immediately to reflect the new collection status.
    The LikeButtonViewModel must publish a status/state property that
    tracks variant collection progress.
    """
    vm_content = _read(LIKE_BUTTON_VM)

    has_published_status = bool(
        re.search(
            r"@Published.*(?:[Cc]ompletion[Ss]tatus|[Cc]ollection[Ss]tate|[Pp]rogress[Ss]tate)",
            vm_content,
        )
    )
    has_status_type = bool(
        re.search(
            r"[Vv]ariant[Ss]?[Cc]ompletion[Ss]tatus|CompletionStatus"
            r"|[Vv]ariant[Cc]ollection[Ss]tate|[Ii]tem[Cc]ollection[Pp]rogress[Ss]tate",
            vm_content,
        )
    )
    assert has_published_status or has_status_type, (
        "LikeButtonViewModel should have a @Published collection status property "
        "(e.g. completionStatus, collectionState, progressState) "
        "that updates when variants are toggled"
    )
