import re
from pathlib import Path

APP = Path("/app/firefox-ios")

BVC_DIR           = APP / "Client/Frontend/Browser/BrowserViewController"
LAYOUT_MANAGER    = BVC_DIR / "BrowserViewControllerLayoutManager.swift"
CONSTRAINT_REF    = BVC_DIR / "ConstraintReference.swift"
BROWSER_VC        = BVC_DIR / "Views/BrowserViewController.swift"
SCROLL_CONTROLLER = APP / "Client/Frontend/Browser/TabScrollController/LegacyTabScrollController.swift"


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def test_layout_manager_file_exists():
    """BrowserViewControllerLayoutManager.swift must be created."""
    assert LAYOUT_MANAGER.exists(), (
        "BrowserViewControllerLayoutManager.swift should exist in the BrowserViewController directory"
    )


def test_layout_manager_uses_nslayoutconstraint():
    """BrowserViewControllerLayoutManager must use native NSLayoutConstraint, not SnapKit."""
    content = _read(LAYOUT_MANAGER)
    assert re.search(r'NSLayoutConstraint', content), (
        "BrowserViewControllerLayoutManager should use NSLayoutConstraint for header layout"
    )
    assert not re.search(r'\.snp\.', content), (
        "BrowserViewControllerLayoutManager should not use SnapKit (.snp.) constraints"
    )


def test_layout_manager_has_setup_and_update_methods():
    """BrowserViewControllerLayoutManager must expose setup and update constraint methods."""
    content = _read(LAYOUT_MANAGER)
    assert re.search(r'func\s+setupHeaderConstraints', content), (
        "BrowserViewControllerLayoutManager should define setupHeaderConstraints"
    )
    assert re.search(r'func\s+updateHeaderConstraints', content), (
        "BrowserViewControllerLayoutManager should define updateHeaderConstraints"
    )


def test_constraint_reference_file_exists():
    """ConstraintReference.swift compatibility shim must be created."""
    assert CONSTRAINT_REF.exists(), (
        "ConstraintReference.swift should exist to bridge SnapKit and NSLayoutConstraint"
    )


def test_constraint_reference_supports_both_snapkit_and_native():
    """ConstraintReference must wrap both SnapKit Constraint and NSLayoutConstraint."""
    content = _read(CONSTRAINT_REF)
    assert re.search(r'init\s*\(.*snapKit\s*:', content, re.DOTALL), (
        "ConstraintReference should have an init(snapKit:) initializer"
    )
    assert re.search(r'init\s*\(.*native\s*:', content, re.DOTALL), (
        "ConstraintReference should have an init(native:) initializer"
    )
    assert re.search(r'func\s+update\s*\(\s*offset\s*:', content), (
        "ConstraintReference should expose an update(offset:) method"
    )


def test_scroll_controller_uses_constraint_reference():
    """LegacyTabScrollController.headerTopConstraint must use ConstraintReference, not raw Constraint."""
    content = _read(SCROLL_CONTROLLER)
    assert re.search(r'headerTopConstraint\s*:\s*ConstraintReference\?', content), (
        "LegacyTabScrollController.headerTopConstraint should be typed as ConstraintReference?"
    )
    assert not re.search(r'headerTopConstraint\s*:\s*Constraint\?', content), (
        "LegacyTabScrollController.headerTopConstraint should no longer be a raw SnapKit Constraint?"
    )


def test_browser_vc_uses_layout_manager():
    """BrowserViewController must instantiate and delegate layout to BrowserViewControllerLayoutManager."""
    content = _read(BROWSER_VC)
    assert re.search(r'BrowserViewControllerLayoutManager', content), (
        "BrowserViewController should instantiate BrowserViewControllerLayoutManager"
    )
    assert re.search(r'browserLayoutManager', content), (
        "BrowserViewController should hold a browserLayoutManager property"
    )
