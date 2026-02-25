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

    func testToastShowLoadingExists() {
        Toast.showLoading("Test")
        Toast.hideLoading()
    }

    func testToastHideLoadingDoesNotCrashWhenNothingShown() {
        Toast.hideLoading()
    }
}
