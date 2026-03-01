import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask2F2PTests: XCTestCase {

    // MARK: - Localization keys return translated strings (not raw keys)

    func testStartTrackingKeyReturnsTranslatedString() {
        let value = NSLocalizedString("START_TRACKING", comment: "")
        XCTAssertEqual(value, "Start Tracking",
                       "START_TRACKING must be localized; raw key indicates missing Localizable.strings")
    }

    func testNoFilesKeyReturnsTranslatedString() {
        let value = NSLocalizedString("NO_FILES", comment: "")
        XCTAssertEqual(value, "No gpx files",
                       "NO_FILES must be localized; raw key indicates missing Localizable.strings")
    }

    func testNoLocationKeyReturnsTranslatedString() {
        let value = NSLocalizedString("NO_LOCATION", comment: "")
        XCTAssertEqual(value, "Not getting location",
                       "NO_LOCATION must be localized; raw key indicates missing Localizable.strings")
    }

    // MARK: - Shared constants use localization system

    func testKNoFilesUsesLocalization() {
        XCTAssertEqual(kNoFiles, NSLocalizedString("NO_FILES", comment: ""),
                       "kNoFiles must use NSLocalizedString for translation support")
    }

    func testKNotGettingLocationTextUsesLocalization() {
        XCTAssertEqual(kNotGettingLocationText, NSLocalizedString("NO_LOCATION", comment: ""),
                       "kNotGettingLocationText must use NSLocalizedString for translation support")
    }

    // MARK: - Additional language support (problem: "at least one additional language")

    func testAdditionalLanguageLocalizationExists() {
        let localizations = Bundle.main.localizations.filter { $0 != "Base" && $0 != "en" }
        var found = false
        for loc in localizations {
            if Bundle.main.path(forResource: "Localizable", ofType: "strings", inDirectory: "\(loc).lproj") != nil {
                found = true
                break
            }
        }
        XCTAssertTrue(found,
                      "At least one additional language (besides English) must have Localizable.strings")
    }

    func testAdditionalLanguageContainsTranslations() {
        let localizations = Bundle.main.localizations.filter { $0 != "Base" && $0 != "en" }
        for loc in localizations {
            guard let path = Bundle.main.path(forResource: "Localizable", ofType: "strings", inDirectory: "\(loc).lproj"),
                  let strings = NSDictionary(contentsOfFile: path) as? [String: String],
                  let startTracking = strings["START_TRACKING"] else { continue }
            XCTAssertNotEqual(startTracking, "START_TRACKING",
                              "\(loc).lproj must contain translated value for START_TRACKING, not raw key")
            return
        }
        XCTFail("No additional language Localizable.strings found with START_TRACKING key")
    }
}
