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
        XCTAssertEqual(kDefaultsKeyKeepScreenAlwaysOn, "KeepScreenAlwaysOn",
                       "UserDefaults key should be 'KeepScreenAlwaysOn'")
    }

    // MARK: - Preferences table section constants

    func testScreenSectionExists() {
        XCTAssertEqual(kScreenSection, 1,
                       "Screen section should be at index 1")
    }

    func testCacheSectionShiftedToIndex2() {
        XCTAssertEqual(kCacheSection, 2,
                       "Cache section should shift to index 2 after screen section insertion")
    }

    func testMapSourceSectionShiftedToIndex3() {
        XCTAssertEqual(kMapSourceSection, 3,
                       "Map source section should shift to index 3")
    }

    // MARK: - Toast loading API

    func testToastDisabledDelayConstant() {
        XCTAssertEqual(Toast.kDisabledDelay, -1.0,
                       "kDisabledDelay should be -1.0 for persistent toasts")
    }

    func testToastShowLoadingExists() {
        Toast.showLoading("Test")
        Toast.hideLoading()
    }

    func testToastHideLoadingDoesNotCrashWhenNothingShown() {
        Toast.hideLoading()
    }
}
