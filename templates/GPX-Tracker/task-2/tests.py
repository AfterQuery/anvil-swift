"""Structural tests for GPX-Tracker task-2: Replace UIAlertView with UIAlertController.

These tests verify only what the problem statement requires:
  1. UIAlertView is no longer instantiated in either file
  2. UIAlertViewDelegate conformance removed from ViewController
  3. Both ViewController and MapViewDelegate use UIAlertController and UIAlertAction
"""

from pathlib import Path

VIEW_CONTROLLER = Path("/app/OpenGpxTracker/ViewController.swift")
MAP_VIEW_DELEGATE = Path("/app/OpenGpxTracker/MapViewDelegate.swift")


def test_no_uialertview_in_viewcontroller():
    """ViewController must not instantiate the deprecated UIAlertView."""
    content = VIEW_CONTROLLER.read_text()
    assert "UIAlertView(" not in content, \
        "ViewController should not instantiate UIAlertView"


def test_no_uialertview_in_mapviewdelegate():
    """MapViewDelegate must not instantiate the deprecated UIAlertView."""
    content = MAP_VIEW_DELEGATE.read_text()
    assert "UIAlertView(" not in content, \
        "MapViewDelegate should not instantiate UIAlertView"


def test_no_uialertviewdelegate_in_viewcontroller():
    """ViewController should not conform to the deprecated UIAlertViewDelegate."""
    content = VIEW_CONTROLLER.read_text()
    assert "UIAlertViewDelegate" not in content, \
        "ViewController should not use UIAlertViewDelegate"


def test_uialertcontroller_used_in_viewcontroller():
    """ViewController should use UIAlertController for alerts."""
    content = VIEW_CONTROLLER.read_text()
    assert "UIAlertController(" in content, \
        "ViewController should use UIAlertController"


def test_uialertaction_used_in_viewcontroller():
    """ViewController should use UIAlertAction for action-based callbacks."""
    content = VIEW_CONTROLLER.read_text()
    assert "UIAlertAction(" in content, \
        "ViewController should use UIAlertAction for button handlers"


def test_uialertcontroller_used_in_mapviewdelegate():
    """MapViewDelegate should use UIAlertController for alerts."""
    content = MAP_VIEW_DELEGATE.read_text()
    assert "UIAlertController(" in content, \
        "MapViewDelegate should use UIAlertController"


def test_uialertaction_used_in_mapviewdelegate():
    """MapViewDelegate should use UIAlertAction for action-based callbacks."""
    content = MAP_VIEW_DELEGATE.read_text()
    assert "UIAlertAction(" in content, \
        "MapViewDelegate should use UIAlertAction for button handlers"
