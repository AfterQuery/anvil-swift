import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask5F2PTests: XCTestCase {

    // MARK: - DefaultDateFormat

    func testDefaultDateFormatProcessesValidInput() {
        let formatter = DefaultDateFormat()
        let result = formatter.getDateFormat(unprocessed: "{dd}-{MMM}-{yyyy}")
        XCTAssertFalse(result.contains("invalid"),
                       "Valid input should produce a non-invalid format string")
    }

    func testDefaultDateFormatRejectsUnterminatedBrace() {
        let formatter = DefaultDateFormat()
        let result = formatter.getDateFormat(unprocessed: "{dd}-{MMM")
        XCTAssertTrue(result.contains("invalid"),
                      "Unterminated brace should be flagged as invalid")
    }

    func testDefaultDateFormatGetDateReturnsNonEmpty() {
        let formatter = DefaultDateFormat()
        let processed = formatter.getDateFormat(unprocessed: "{dd}-{MMM}-{yyyy}")
        let date = formatter.getDate(processedFormat: processed)
        XCTAssertFalse(date.isEmpty, "Formatted date should not be empty")
    }

    // MARK: - DateField struct

    func testDateFieldStructExists() {
        let field = DateField(type: "Year", patterns: ["YY", "YYYY"], subtitles: nil)
        XCTAssertEqual(field.type, "Year")
        XCTAssertEqual(field.patterns.count, 2)
    }

    // MARK: - String extension

    func testCountInstancesExtension() {
        let str = "hello world hello"
        XCTAssertEqual(str.countInstances(of: "hello"), 2)
    }

    // MARK: - Preferences section constant

    func testDefaultNameSectionExists() {
        XCTAssertEqual(kDefaultNameSection, 4,
                       "Default name section should be at index 4")
    }

    func testSectionCountIncreasedTo5() {
        let vc = PreferencesTableViewController(style: .grouped)
        let sections = vc.numberOfSections(in: vc.tableView)
        XCTAssertEqual(sections, 5,
                       "Preferences should have 5 sections after adding default name")
    }

    // MARK: - DefaultNameSetupViewController

    func testDefaultNameSetupViewControllerExists() {
        let vc = DefaultNameSetupViewController(style: .grouped)
        XCTAssertNotNil(vc)
    }
}
