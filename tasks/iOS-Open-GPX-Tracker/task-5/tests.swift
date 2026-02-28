import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask5F2PTests: XCTestCase {

    // MARK: - DefaultDateFormat

    func testDefaultDateFormatProcessesValidInput() {
        let formatter = DefaultDateFormat()
        let processed = formatter.getDateFormat(unprocessed: "{dd}-{MMM}-{yyyy}")
        let date = formatter.getDate(processedFormat: processed)
        XCTAssertFalse(date.isEmpty,
                       "Valid input should produce a non-empty formatted date")
    }

    func testDefaultDateFormatHandlesUnterminatedBrace() {
        let formatter = DefaultDateFormat()
        let invalidResult = formatter.getDate(processedFormat: formatter.getDateFormat(unprocessed: "{dd}-{MMM"))
        let validResult = formatter.getDate(processedFormat: formatter.getDateFormat(unprocessed: "{dd}-{MMM}-{yyyy}"))
        XCTAssertNotEqual(invalidResult, validResult,
                          "Malformed input should not produce the same formatted date as valid input")
    }

    func testInvalidFormatDoesNotCrash() {
        let formatter = DefaultDateFormat()
        let invalidFormats = ["{dd}-{MMM", "{{broken", "}", "invalid{dd", ""]
        for invalid in invalidFormats {
            let processed = formatter.getDateFormat(unprocessed: invalid)
            _ = formatter.getDate(processedFormat: processed)
            // Must not crash; if we get here, the test passes
        }
    }

    func testDefaultDateFormatProducesRecognizableDateStructure() {
        let formatter = DefaultDateFormat()
        let processed = formatter.getDateFormat(unprocessed: "{dd}-{MMM}-{yyyy}")
        let date = formatter.getDate(processedFormat: processed)
        XCTAssertFalse(date.isEmpty, "Formatted date should not be empty")
        // Output should look like "25-Feb-2025" — digits, separator, letters, separator, digits
        let components = date.split(separator: "-")
        XCTAssertEqual(components.count, 3,
                       "dd-MMM-yyyy format should produce 3 hyphen-separated components")
        XCTAssertTrue(components[0].allSatisfy(\.isNumber), "Day component should be numeric")
        XCTAssertTrue(components[2].allSatisfy(\.isNumber), "Year component should be numeric")
    }

    // MARK: - DateField struct

    func testDateFieldStructExists() {
        let field = DateField(type: "Year", patterns: ["YY", "YYYY"], subtitles: nil)
        XCTAssertEqual(field.type, "Year")
        XCTAssertEqual(field.patterns.count, 2)
    }

    func testDateFieldSubtitlesDictionary() {
        let field = DateField(type: "Month", patterns: ["M", "MM"], subtitles: ["M": "Single", "MM": "Padded"])
        XCTAssertEqual(field.subtitles?["M"], "Single")
        XCTAssertEqual(field.subtitles?["MM"], "Padded")
    }

    // MARK: - String extension

    func testCountInstancesExtension() {
        let str = "hello world hello"
        XCTAssertEqual(str.countInstances(of: "hello"), 2)
    }

    // MARK: - Preferences section constant

    func testDefaultNameSectionExists() {
        XCTAssertGreaterThanOrEqual(kDefaultNameSection, 0,
                                    "Default name section should be a valid section index")
    }

    func testSectionCountIncludesDefaultName() {
        let vc = PreferencesTableViewController(style: .grouped)
        vc.loadViewIfNeeded()
        let sections = vc.numberOfSections(in: vc.tableView)
        XCTAssertGreaterThanOrEqual(sections, 5,
                                    "Preferences should have at least 5 sections after adding default name")
    }

    // MARK: - DefaultNameSetupViewController

    func testDefaultNameSetupViewControllerExists() {
        let vc = DefaultNameSetupViewController(style: .grouped)
        XCTAssertNotNil(vc)
    }

    func testDefaultNameSetupViewControllerHasDateFormatSetupContent() {
        let vc = DefaultNameSetupViewController(style: .grouped)
        vc.loadViewIfNeeded()
        let sections = vc.numberOfSections(in: vc.tableView)
        XCTAssertGreaterThanOrEqual(sections, 1,
                                   "DefaultNameSetupViewController should have at least one section for date format setup")
    }
}
