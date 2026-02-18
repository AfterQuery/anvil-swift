#!/bin/bash
set -e

cd /app

# Create test directory preserving original structure
mkdir -p tasks/task-3

cat > tasks/task-3/task_tests.py << 'ANVIL_TEST_CODE'
import re
from pathlib import Path

VIEW_CONTROLLER = Path("/app/OpenGpxTracker/ViewController.swift")


def test_mkscaleview_used():
    """ViewController must use MKScaleView as the map scale bar."""
    content = VIEW_CONTROLLER.read_text()
    assert "MKScaleView" in content, \
        "ViewController should use MKScaleView for the scale bar"


def test_scalebar_added_to_view():
    """The scale bar must be added to the view hierarchy."""
    content = VIEW_CONTROLLER.read_text()
    assert re.search(r'addSubview\(\w*[sS]cale\w*\)', content), \
        "Scale bar should be added to the view via addSubview"


def test_scalebar_connected_to_map():
    """The scale bar must be connected to the map view so it reflects zoom level."""
    content = VIEW_CONTROLLER.read_text()
    has_mapview_assignment = bool(re.search(r'\w*[sS]cale\w*\.mapView\s*=\s*map', content))
    has_init_with_map = bool(re.search(r'MKScaleView\(mapView:\s*(?:self\.)?map', content))
    assert has_mapview_assignment or has_init_with_map, \
        "Scale bar should be connected to the map (via .mapView or init)"


def test_location_check_uses_authorization_status():
    """The location check should use authorizationStatus, not the deprecated class method."""
    content = VIEW_CONTROLLER.read_text()
    has_equality_check = bool(re.search(r'authorizationStatus\s*==\s*\.denied', content))
    has_switch_case = bool(re.search(r'authorizationStatus', content)) and bool(
        re.search(r'case\s+\.denied', content))
    assert has_equality_check or has_switch_case, \
        "Location check should use authorizationStatus with .denied (via == or switch/case)"


def test_deprecated_location_services_removed():
    """The deprecated CLLocationManager.locationServicesEnabled() guard should be replaced."""
    content = VIEW_CONTROLLER.read_text()
    assert not re.search(r'guard\s+CLLocationManager\.locationServicesEnabled\(\)', content), \
        "Deprecated guard CLLocationManager.locationServicesEnabled() should be removed"


def test_unnecessary_availability_checks_removed():
    """Obsolete #available(iOS 10/11) checks should be removed since the deployment target has moved past them."""
    content = VIEW_CONTROLLER.read_text()
    assert not re.search(r'#available\(iOS\s+10', content), \
        "Unnecessary #available(iOS 10, *) checks should be removed"
    ios11_count = len(re.findall(r'#available\(iOS\s+11', content))
    assert ios11_count <= 1, \
        f"Found {ios11_count} #available(iOS 11, *) checks; at most 1 (safe-area) should remain"

ANVIL_TEST_CODE

python3 -m pytest -v tasks/task-3/task_tests.py 2>&1 || true
