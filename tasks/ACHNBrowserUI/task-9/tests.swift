import XCTest
@testable import AC_Helper

final class AnvilTask9F2PTests: XCTestCase {

    // MARK: - Traditional Chinese locale identifier

    func testTraditionalChineseLocaleExists() {
        let path = Bundle.main.path(forResource: "zh-Hant-TW", ofType: "lproj")
        XCTAssertNotNil(path, "zh-Hant-TW.lproj should exist as a valid locale")
    }

    func testDeprecatedZHTWLocaleRemoved() {
        let path = Bundle.main.path(forResource: "ZH_TW", ofType: "lproj")
        XCTAssertNil(path, "Deprecated ZH_TW.lproj should be removed")
    }

    // MARK: - Key casing fix

    func testGermanWeddingSeasonKeyMatchesAppCode() {
        guard let dePath = Bundle.main.path(forResource: "de", ofType: "lproj"),
              let deBundle = Bundle(path: dePath) else {
            XCTFail("de.lproj should exist")
            return
        }
        let translation = deBundle.localizedString(
            forKey: "Wedding season",
            value: "MISSING",
            table: nil
        )
        XCTAssertNotEqual(translation, "MISSING",
                          "German should have a translation for 'Wedding season' (lowercase s)")
    }
}
