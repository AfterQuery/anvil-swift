import re
from pathlib import Path

ROOT = Path("/app/ACHNBrowserUI")

USER_COLLECTION = ROOT / "Packages/Backend/Sources/Backend/Environments/UserCollection.swift"
ITEM = ROOT / "Packages/Backend/Sources/Backend/Models/Item.swift"
ITEM_DETAIL_VIEW = ROOT / "ACHNBrowserUI/views/items/detail/ItemDetailView.swift"
LIKE_BUTTON_VIEW = ROOT / "ACHNBrowserUI/views/shared/LikeButtonView.swift"
LIKE_BUTTON_VM = ROOT / "ACHNBrowserUI/viewModels/LikeButtonViewModel.swift"
VARIANTS_FOR_LIKE_VIEW = ROOT / "ACHNBrowserUI/views/shared/VariantsForLikeView.swift"


def _read(path):
    return path.read_text() if path.exists() else ""


# ---------------------------------------------------------------------------
# Test 1 — UserCollection tracks variant completion status
# ---------------------------------------------------------------------------


def test_user_collection_tracks_variant_completion():
    """UserCollection must have a way to determine the like status based on
    variant completion. Accepts methods like:
      - completionStatus(for: Item)
      - variantCompletionStatus(for: Item)
      - getItemLikeStatus(item: Item)
      - isPartiallyLiked(item: Item)
      - variantsLikedCount(for: Item)
    """
    content = _read(USER_COLLECTION)
    has_completion_check = bool(
        re.search(
            r"func\s+\w*(?:[Cc]ompletion|[Ss]tatus|[Ll]iked[Cc]ount|[Ll]ike[Ss]tatus)\w*\s*\(",
            content,
        )
    )
    has_variant_tracking = bool(
        re.search(r"[Ll]iked[Vv]ariants|variant.*\[.*\]|variantIds", content)
    )
    assert has_completion_check or has_variant_tracking, (
        "UserCollection should track which variants are liked for each item "
        "and provide a way to check completion status"
    )


# ---------------------------------------------------------------------------
# Test 2 — Item model has variant information
# ---------------------------------------------------------------------------


def test_item_has_variant_properties():
    """Item must expose variant information. Accepts:
    - variations: [Variant] property
    - variants: [Variant] property
    - hasVariants / hasSomeVariations: Bool property
    """
    content = _read(ITEM)
    uc_content = _read(USER_COLLECTION)
    all_content = content + uc_content

    has_variations_prop = bool(
        re.search(r"(?:var|let)\s+variations\s*:", content)
    )
    has_variants_prop = bool(
        re.search(r"(?:var|let)\s+variants\s*:", content)
    )
    has_variant_check = bool(
        re.search(
            r"(?:var|let)\s+\w*(?:[Hh]as[Vv]ariant|[Hh]as[Ss]ome[Vv]ariation)\w*\s*:",
            all_content,
        )
    )
    assert has_variations_prop or has_variants_prop or has_variant_check, (
        "Item should have properties to access variant information "
        "(e.g. variations: [Variant], hasSomeVariations: Bool)"
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
        re.search(r"\.sheet\(|\.modal\(|@State.*showVariant|@Binding.*item", all_content)
    )
    assert has_variant_view or has_modal, (
        "A variant selection view should exist "
        "(e.g. VariantsForLikeView, VariantSelectionSheet)"
    )


# ---------------------------------------------------------------------------
# Test 5 — ItemDetail favorite button triggers variant selection
# ---------------------------------------------------------------------------


def test_item_detail_favorite_button_shows_variants():
    """When an item with variants is tapped on the favorite button in
    ItemDetail, it should show the variant selection view instead of just
    toggling the parent item.
    """
    content = _read(ITEM_DETAIL_VIEW)

    has_variant_trigger = bool(
        re.search(
            r"itemToDisplayVariantsLike|likedItemWithVariants|showVariant|presentVariant",
            content,
            re.IGNORECASE,
        )
    )
    has_variation_check = bool(
        re.search(
            r"hasSomeVariations|hasVariants|variant.*sheet|VariantsForLike",
            content,
            re.IGNORECASE,
        )
    )
    assert has_variant_trigger or has_variation_check, (
        "ItemDetailView should trigger variant selection when "
        "favorite button is tapped for multi-variant items"
    )


# ---------------------------------------------------------------------------
# Test 6 — Parent item synced with variants (auto-add on first like)
# ---------------------------------------------------------------------------


def test_parent_item_synced_on_variant_like():
    """When the first variant of an item is liked, the parent item should
    automatically be added to the collection.
    """
    content = _read(USER_COLLECTION)

    has_sync_logic = bool(
        re.search(
            r"first.*variant|variant.*added|parent.*sync|add.*parent|toggleItem",
            content,
            re.IGNORECASE,
        )
    )
    has_variant_update = bool(
        re.search(
            r"update.*variant|variant.*change|addVariant|completionStatus.*unstarted",
            content,
        )
    )
    assert has_sync_logic or has_variant_update, (
        "UserCollection should have logic to sync parent item with variants "
        "(auto-add parent when first variant is liked)"
    )


# ---------------------------------------------------------------------------
# Test 7 — Items without variants don't use partial like system
# ---------------------------------------------------------------------------


def test_items_without_variants_unaffected():
    """Items with zero or one variant should not display the partial like
    system. Only items with 2+ variants should show half-star state.
    """
    uc_content = _read(USER_COLLECTION)
    item_content = _read(ITEM)
    vm_content = _read(LIKE_BUTTON_VM)
    all_content = uc_content + item_content + vm_content

    has_variant_count_check = bool(
        re.search(
            r"variations?\??\.count.*[<>=]|variant[Cc]ount.*[<>=]|\bvariantCount\b",
            all_content,
        )
    )
    has_multi_variant_check = bool(
        re.search(
            r"variations?\??\.count\s*.*[>].*1|hasSomeVariations|hasMultiple[Vv]ariants",
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
    """When variants are toggled in the variant selection view, the half-star
    icon should update immediately to reflect the new completion status.
    """
    sheet_content = _read(VARIANTS_FOR_LIKE_VIEW)
    detail_content = _read(ITEM_DETAIL_VIEW)
    vm_content = _read(LIKE_BUTTON_VM)

    all_content = sheet_content + detail_content + vm_content

    has_state_update = bool(
        re.search(
            r"\.onChange|\.onReceive|didSet.*variant|update.*like|refresh.*state|completionStatus",
            all_content,
            re.IGNORECASE,
        )
    )
    has_reactive = bool(
        re.search(r"@State|@Published|@ObservedObject|@StateObject|@Binding", all_content)
    )
    assert has_state_update or has_reactive, (
        "The variant selection view should trigger updates to the like state "
        "observable when variants are toggled"
    )
