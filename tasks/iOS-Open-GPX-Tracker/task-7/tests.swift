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

    func testKeepScreenAlwaysOnPersistsToUserDefaults() {
        let prefs = Preferences.shared
        let original = prefs.keepScreenAlwaysOn
        prefs.keepScreenAlwaysOn = true
        XCTAssertTrue(UserDefaults.standard.bool(forKey: kDefaultsKeyKeepScreenAlwaysOn),
                      "keepScreenAlwaysOn must persist to UserDefaults for restoration on app launch")
        prefs.keepScreenAlwaysOn = original
    }

    // MARK: - Preferences table section constants

    func testScreenSectionExists() {
        XCTAssertGreaterThanOrEqual(kScreenSection, 0,
                                    "Screen section should be a valid section index")
    }

    // MARK: - Toast loading API

    func testToastDisabledDelayConstantExists() {
        XCTAssertTrue(Toast.kDisabledDelay.isFinite,
                      "kDisabledDelay must exist and be a valid numeric value for loading toast configuration")
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
