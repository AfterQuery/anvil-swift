import re
from pathlib import Path

APP = Path("/app/firefox-ios")

RELAY_SETTINGS = APP / "Client/Frontend/Settings/RelayMaskSettingsViewController.swift"
SETTINGS_COORD = APP / "Client/Coordinators/SettingsCoordinator.swift"
RELAY_TESTS    = (APP / "firefox-ios-tests/Tests/ClientTests/Settings"
                  / "RelayMaskSettingsViewControllerTests.swift")


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def test_relay_settings_vc_accepts_tab_manager():
    """RelayMaskSettingsViewController init must accept a tabManager parameter."""
    content = _read(RELAY_SETTINGS)
    assert re.search(r'init\s*\(.*tabManager\s*:', content, re.DOTALL), (
        "RelayMaskSettingsViewController init should accept a tabManager parameter"
    )


def test_manage_masks_opens_new_tab_not_webview():
    """ManageRelayMasksSetting.onClick must open a browser tab, not push a SettingsContentViewController."""
    content = _read(RELAY_SETTINGS)
    assert re.search(r'addTabsForURLs', content), (
        "ManageRelayMasksSetting.onClick should call tabManager.addTabsForURLs to open a new tab"
    )
    assert "SettingsContentViewController" not in content, (
        "ManageRelayMasksSetting.onClick should not open a SettingsContentViewController (embedded webview)"
    )


def test_settings_dismissed_after_opening_tab():
    """Settings must be dismissed after opening the Relay URL in a new tab."""
    content = _read(RELAY_SETTINGS)
    assert re.search(r'dismissVC\(\)', content), (
        "RelayMaskSettingsViewController should dismiss itself after opening the new tab"
    )


def test_settings_coordinator_passes_tab_manager():
    """SettingsCoordinator must pass tabManager when creating RelayMaskSettingsViewController."""
    content = _read(SETTINGS_COORD)
    assert re.search(r'RelayMaskSettingsViewController\s*\(.*tabManager\s*:', content, re.DOTALL), (
        "SettingsCoordinator should pass tabManager to RelayMaskSettingsViewController"
    )


def test_relay_mask_url_is_relay_account_management():
    """The URL opened must be the Relay account management URL."""
    content = _read(RELAY_SETTINGS)
    assert re.search(r'URLForRelayAccountManagement', content), (
        "ManageRelayMasksSetting should use SupportUtils.URLForRelayAccountManagement"
    )


def test_relay_settings_unit_tests_added():
    """Unit test file for RelayMaskSettingsViewController must be present."""
    assert RELAY_TESTS.exists(), (
        f"Unit test file RelayMaskSettingsViewControllerTests.swift should exist at {RELAY_TESTS}"
    )
    content = _read(RELAY_TESTS)
    assert re.search(r'func\s+test\w+', content), (
        "RelayMaskSettingsViewControllerTests.swift should contain at least one test function"
    )
