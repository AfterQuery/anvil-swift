"""Structural tests for GPX-Tracker task-3: Add MapKit scale bar and fix location check.

These tests verify only what the problem statement requires:
  1. MKScaleView is used as the scale bar
  2. The scale bar is added to the view hierarchy and connected to the map
  3. The location status check uses authorizationStatus instead of the deprecated API
  4. The deprecated CLLocationManager.locationServicesEnabled() call is removed
  5. Unnecessary iOS version availability checks are removed
"""

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
    has_init_with_map = bool(re.search(r'MKScaleView\(mapView:\s*map', content))
    assert has_mapview_assignment or has_init_with_map, \
        "Scale bar should be connected to the map (via .mapView or init)"


def test_location_check_uses_authorization_status():
    """The location check should use authorizationStatus, not the deprecated class method."""
    content = VIEW_CONTROLLER.read_text()
    assert re.search(r'authorizationStatus\s*==\s*\.denied', content), \
        "Location check should use authorizationStatus == .denied"


def test_deprecated_location_services_removed():
    """The deprecated CLLocationManager.locationServicesEnabled() should no longer be used."""
    content = VIEW_CONTROLLER.read_text()
    assert "CLLocationManager.locationServicesEnabled()" not in content, \
        "Deprecated CLLocationManager.locationServicesEnabled() should be removed"


def test_unnecessary_availability_checks_removed():
    """Obsolete #available(iOS 10/11) checks should be removed since the deployment target has moved past them."""
    content = VIEW_CONTROLLER.read_text()
    assert not re.search(r'#available\(iOS\s+10', content), \
        "Unnecessary #available(iOS 10, *) checks should be removed"
    assert not re.search(r'#available\(iOS\s+11', content), \
        "Unnecessary #available(iOS 11, *) checks should be removed"
