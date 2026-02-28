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

    // MARK: - Additional language support

    func testGermanLocalizationExists() {
        let path = Bundle.main.path(forResource: "Localizable", ofType: "strings", inDirectory: "de.lproj")
        XCTAssertNotNil(path,
                        "de.lproj/Localizable.strings must exist for German localization")
    }

    func testGermanLocalizationContainsTranslations() {
        guard let dePath = Bundle.main.path(forResource: "Localizable", ofType: "strings", inDirectory: "de.lproj"),
              let deStrings = NSDictionary(contentsOfFile: dePath) as? [String: String],
              let deStartTracking = deStrings["START_TRACKING"] else {
            XCTFail("German Localizable.strings must exist and contain START_TRACKING")
            return
        }
        XCTAssertNotEqual(deStartTracking, "START_TRACKING",
                          "German file must contain translated value, not raw key")
    }
}
