import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask7F2PTests: XCTestCase {

    // MARK: - Preferences: keepScreenAlwaysOn

    func testKeepScreenAlwaysOnDefaultsToFalse() {
        let prefs = Preferences.shared
        XCTAssertFalse(prefs.keepScreenAlwaysOn,
                       "keepScreenAlwaysOn should default to false")
    }

    func testKeepScreenAlwaysOnCanBeToggled() {
        let prefs = Preferences.shared
        let original = prefs.keepScreenAlwaysOn
        prefs.keepScreenAlwaysOn = !original
        XCTAssertEqual(prefs.keepScreenAlwaysOn, !original)
        prefs.keepScreenAlwaysOn = original
    }

    func testKeepScreenAlwaysOnDefaultsKey() {
        XCTAssertFalse(kDefaultsKeyKeepScreenAlwaysOn.isEmpty,
                       "UserDefaults key should be a non-empty string")
    }

    // MARK: - Preferences table section constants

    func testScreenSectionExists() {
        XCTAssertGreaterThanOrEqual(kScreenSection, 0,
                                    "Screen section should be a valid section index")
    }

    func testScreenSectionPrecedesCacheSection() {
        XCTAssertLessThan(kScreenSection, kCacheSection,
                          "Screen section should appear before cache section")
    }

    // MARK: - Toast loading API

    func testToastDisabledDelayConstant() {
        XCTAssertLessThan(Toast.kDisabledDelay, 0,
                          "kDisabledDelay should be negative to signal a persistent toast")
    }

    func testToastShowLoadingAddsViewToWindow() {
        guard let window = UIApplication.shared.windows.first else {
            XCTFail("No window available in test environment")
            return
        }
        Toast.hideLoading()
        let before = window.subviews.count
        Toast.showLoading("Test")
        let after = window.subviews.count
        XCTAssertGreaterThan(after, before,
                             "Toast.showLoading should add a visible subview to the window")
        Toast.hideLoading()
    }

    func testToastShowLoadingPersistsUntilHidden() {
        guard let window = UIApplication.shared.windows.first else {
            XCTFail("No window available in test environment")
            return
        }
        Toast.hideLoading()
        let before = window.subviews.count
        Toast.showLoading("Persistent test")
        let duringCount = window.subviews.count
        XCTAssertGreaterThan(duringCount, before,
                             "Loading toast should remain visible")
        Toast.hideLoading()
    }

    func testToastHideLoadingDoesNotCrashWhenNothingShown() {
        Toast.hideLoading()
    }

    // MARK: - keepScreenAlwaysOn wires to idle timer

    func testKeepScreenAlwaysOnDisablesIdleTimerWhenViewControllerLoads() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let vc = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Could not load ViewController from storyboard")
            return
        }
        let prefs = Preferences.shared
        let original = prefs.keepScreenAlwaysOn
        prefs.keepScreenAlwaysOn = true
        vc.loadViewIfNeeded()
        XCTAssertTrue(UIApplication.shared.isIdleTimerDisabled,
                      "When keepScreenAlwaysOn is true, isIdleTimerDisabled must be set so screen stays on")
        prefs.keepScreenAlwaysOn = original
        if !original {
            UIApplication.shared.isIdleTimerDisabled = false
        }
    }
}
