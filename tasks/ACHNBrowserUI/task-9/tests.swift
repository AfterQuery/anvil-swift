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

    func testDeprecatedLowercaseZhTwLocaleRemoved() {
        let path = Bundle.main.path(forResource: "zh_tw", ofType: "lproj")
        XCTAssertNil(path, "Deprecated zh_tw.lproj should be removed")
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

    // MARK: - Japanese InfoPlist.strings removed

    func testJapaneseInfoPlistStringsRemoved() {
        guard let jaPath = Bundle.main.path(forResource: "ja", ofType: "lproj"),
              let jaBundle = Bundle(path: jaPath) else {
            XCTFail("ja.lproj should exist for Localizable.strings")
            return
        }
        let infoPlistPath = jaBundle.path(forResource: "InfoPlist", ofType: "strings")
        XCTAssertNil(infoPlistPath,
                     "Japanese InfoPlist.strings should be removed (it contained incorrect German text)")
    }

    func testJapaneseLocalizableStringsStillExists() {
        guard let jaPath = Bundle.main.path(forResource: "ja", ofType: "lproj"),
              let jaBundle = Bundle(path: jaPath) else {
            XCTFail("ja.lproj should exist")
            return
        }
        let localizablePath = jaBundle.path(forResource: "Localizable", ofType: "strings")
        XCTAssertNotNil(localizablePath,
                        "Japanese Localizable.strings should still exist")
    }

    // MARK: - Italian InfoPlist.strings exists in variant group

    func testItalianInfoPlistStringsExists() {
        guard let itPath = Bundle.main.path(forResource: "it", ofType: "lproj"),
              let itBundle = Bundle(path: itPath) else {
            XCTFail("it.lproj should exist")
            return
        }
        let infoPlistPath = itBundle.path(forResource: "InfoPlist", ofType: "strings")
        XCTAssertNotNil(infoPlistPath,
                        "Italian InfoPlist.strings should exist")
    }

    // MARK: - German locale loads correctly after deduplication

    func testGermanLocalizableStringsLoads() {
        guard let dePath = Bundle.main.path(forResource: "de", ofType: "lproj"),
              let deBundle = Bundle(path: dePath) else {
            XCTFail("de.lproj should exist")
            return
        }
        let translation = deBundle.localizedString(forKey: "Settings", value: "MISSING", table: nil)
        XCTAssertNotEqual(translation, "MISSING",
                          "German Localizable.strings should parse and load translations after deduplication")
    }

    func testGermanLabelleSurvivesDuplicateCleanup() {
        guard let dePath = Bundle.main.path(forResource: "de", ofType: "lproj"),
              let deBundle = Bundle(path: dePath) else {
            XCTFail("de.lproj should exist")
            return
        }
        let translation = deBundle.localizedString(forKey: "Labelle", value: "MISSING", table: nil)
        XCTAssertNotEqual(translation, "MISSING",
                          "Labelle should still have a German translation after duplicate cleanup")
    }

    // MARK: - French duplicate keys removed

    func testFrenchNoResultsTranslation() {
        guard let frPath = Bundle.main.path(forResource: "fr", ofType: "lproj"),
              let frBundle = Bundle(path: frPath) else {
            XCTFail("fr.lproj should exist")
            return
        }
        let translation = frBundle.localizedString(
            forKey: "No results for %@",
            value: "MISSING",
            table: nil
        )
        XCTAssertNotEqual(translation, "MISSING")
        XCTAssertEqual(translation, "Pas de résultats pour %@",
                       "French should have exactly one consistent translation for 'No results for %@'")
    }

    func testFrenchSpaceSurvivesDuplicateCleanup() {
        guard let frPath = Bundle.main.path(forResource: "fr", ofType: "lproj"),
              let frBundle = Bundle(path: frPath) else {
            XCTFail("fr.lproj should exist")
            return
        }
        let translation = frBundle.localizedString(forKey: "Space", value: "MISSING", table: nil)
        XCTAssertNotEqual(translation, "MISSING",
                          "Space should still have a French translation after duplicate removal")
        XCTAssertEqual(translation, "Éspace",
                       "The correct French translation for Space should survive deduplication")
    }

    // MARK: - Italian locale loads properly

    func testItalianLocalizableStringsLoads() {
        guard let itPath = Bundle.main.path(forResource: "it", ofType: "lproj"),
              let itBundle = Bundle(path: itPath) else {
            XCTFail("it.lproj should exist")
            return
        }
        let translation = itBundle.localizedString(
            forKey: "Settings",
            value: "MISSING",
            table: nil
        )
        XCTAssertNotEqual(translation, "MISSING",
                          "Italian Localizable.strings should parse correctly and load translations")
    }
}
