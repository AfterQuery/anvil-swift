import re
from pathlib import Path

VIEW_CONTROLLER = Path("/app/OpenGpxTracker/ViewController.swift")


def _read(path):
    return path.read_text() if path.exists() else ""


def test_auto_layout_constraints_used():
    """Layout must use Auto Layout constraints instead of manual frame math."""
    content = _read(VIEW_CONTROLLER)
    nslayout_count = len(re.findall(r'NSLayoutConstraint\(', content))
    anchor_count = len(re.findall(r'\.constraint\(', content))
    activate_count = len(re.findall(r'NSLayoutConstraint\.activate\(', content))
    total = nslayout_count + anchor_count + activate_count
    assert total >= 10, (
        f"Expected at least 10 Auto Layout constraint usages "
        f"(NSLayoutConstraint init, anchor .constraint, or .activate), found {total}"
    )


def test_translates_autoresizing_mask_disabled():
    """Key UI elements must set translatesAutoresizingMaskIntoConstraints = false."""
    content = _read(VIEW_CONTROLLER)
    disabled_count = len(re.findall(
        r'translatesAutoresizingMaskIntoConstraints\s*=\s*false', content))
    assert disabled_count >= 8, (
        f"Expected at least 8 elements with translatesAutoresizingMaskIntoConstraints = false, "
        f"found {disabled_count}"
    )


def test_no_hardcoded_button_frames():
    """Buttons must not use hardcoded frame/center assignments for positioning."""
    content = _read(VIEW_CONTROLLER)
    button_frame_patterns = [
        r'trackerButton\.frame\s*=\s*CGRect',
        r'trackerButton\.center\s*=\s*CGPoint',
        r'newPinButton\.frame\s*=\s*CGRect',
        r'newPinButton\.center\s*=\s*CGPoint',
        r'followUserButton\.frame\s*=\s*CGRect',
        r'followUserButton\.center\s*=\s*CGPoint',
        r'saveButton\.frame\s*=\s*CGRect',
        r'saveButton\.center\s*=\s*CGPoint',
        r'resetButton\.frame\s*=\s*CGRect',
        r'resetButton\.center\s*=\s*CGPoint',
    ]
    for pattern in button_frame_patterns:
        assert not re.search(pattern, content), (
            f"Button should not use hardcoded frame/center: pattern '{pattern}' found"
        )


def test_autoresizing_mask_removed_from_buttons_and_labels():
    """autoresizingMask should not be set on the buttons or status labels."""
    content = _read(VIEW_CONTROLLER)
    elements = [
        'trackerButton', 'newPinButton', 'followUserButton',
        'saveButton', 'resetButton', 'appTitleLabel', 'coordsLabel',
        'timeLabel', 'speedLabel', 'totalTrackedDistanceLabel',
        'currentSegmentDistanceLabel',
    ]
    for elem in elements:
        assert not re.search(rf'{elem}\.autoresizingMask\s*=', content), (
            f"{elem}.autoresizingMask should be removed; use Auto Layout constraints instead"
        )


def test_label_frames_removed():
    """Status labels should not use hardcoded frame assignments."""
    content = _read(VIEW_CONTROLLER)
    label_frame_patterns = [
        r'appTitleLabel\.frame\s*=\s*CGRect',
        r'coordsLabel\.frame\s*=\s*CGRect',
        r'timeLabel\.frame\s*=\s*CGRect',
        r'speedLabel\.frame\s*=\s*CGRect',
        r'totalTrackedDistanceLabel\.frame\s*=\s*CGRect',
        r'currentSegmentDistanceLabel\.frame\s*=\s*CGRect',
    ]
    for pattern in label_frame_patterns:
        assert not re.search(pattern, content), (
            f"Label should not use hardcoded frame: pattern '{pattern}' found"
        )


def test_view_will_transition_implemented():
    """viewWillTransition(to:with:) must be overridden for orientation handling."""
    content = _read(VIEW_CONTROLLER)
    assert re.search(
        r'override\s+func\s+viewWillTransition\s*\(\s*to\s+\w+\s*:\s*CGSize',
        content
    ), "ViewController should override viewWillTransition(to:with:) for orientation changes"


def test_compass_repositioned_on_orientation_change():
    """The compass must be repositioned when the device orientation changes."""
    content = _read(VIEW_CONTROLLER)
    vwt_match = re.search(
        r'func\s+viewWillTransition\s*\([^)]*\)\s*\{', content)
    assert vwt_match, "viewWillTransition must be implemented"
    window = content[vwt_match.start():vwt_match.start() + 800]
    assert re.search(r'compass', window, re.IGNORECASE), (
        "viewWillTransition should reposition the compass"
    )
