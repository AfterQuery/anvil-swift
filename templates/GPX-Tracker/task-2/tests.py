from pathlib import Path
import re

ROOT = Path("/app/OpenGpxTracker")

# Files that use UIAlertView in the base code and must be migrated
MIGRATED_FILES = [
    ROOT / "MapViewDelegate.swift",
    ROOT / "ViewController.swift",
]


def swift_files():
    return list(ROOT.rglob("*.swift"))


def all_code():
    return "\n".join(p.read_text() for p in swift_files())


def migrated_code():
    return "\n".join(p.read_text() for p in MIGRATED_FILES if p.exists())


def test_no_uialertview_usage():
    """Deprecated UIAlertView must be fully removed."""
    code = all_code()
    assert "UIAlertView" not in code, "UIAlertView should not be used anywhere"


def test_no_uialertviewdelegate_usage():
    """UIAlertViewDelegate should not remain after migration."""
    code = all_code()
    assert "UIAlertViewDelegate" not in code, "UIAlertViewDelegate should be removed"


def test_modern_alert_api_present():
    """
    Each migrated file must use UIAlertController for presenting alerts.

    Checked per-file so that pre-existing UIAlertController usage in one
    file cannot mask a missing migration in another.
    """
    for path in MIGRATED_FILES:
        code = path.read_text() if path.exists() else ""
        count = code.count("UIAlertController")
        assert count >= 1, (
            f"{path.name} should use UIAlertController after migration"
        )


def test_action_handlers_used():
    """
    Each migrated file should use action handlers instead of delegate callbacks.

    Checked per-file to ensure every file that had UIAlertView delegate
    callbacks now uses UIAlertAction handlers or handler closures.
    """
    for path in MIGRATED_FILES:
        code = path.read_text() if path.exists() else ""
        has_action = "UIAlertAction" in code
        has_handler = bool(re.search(r"handler\s*:\s*\{", code))
        assert has_action or has_handler, (
            f"{path.name} should use action handlers instead of delegate callbacks"
        )
