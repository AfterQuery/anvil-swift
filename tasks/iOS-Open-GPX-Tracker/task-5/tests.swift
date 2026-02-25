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

    func testDefaultDateFormatRejectsUnterminatedBrace() {
        let formatter = DefaultDateFormat()
        let validResult = formatter.getDateFormat(unprocessed: "{dd}-{MMM}-{yyyy}")
        let invalidResult = formatter.getDateFormat(unprocessed: "{dd}-{MMM")
        XCTAssertNotEqual(validResult, invalidResult,
                          "Malformed input should produce a different result than valid input")
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
        XCTAssertGreaterThanOrEqual(kDefaultNameSection, 0,
                                    "Default name section should be a valid section index")
    }

    func testSectionCountIncludesDefaultName() {
        let vc = PreferencesTableViewController(style: .grouped)
        let sections = vc.numberOfSections(in: vc.tableView)
        XCTAssertGreaterThanOrEqual(sections, 5,
                                    "Preferences should have at least 5 sections after adding default name")
    }

    // MARK: - DefaultNameSetupViewController

    func testDefaultNameSetupViewControllerExists() {
        let vc = DefaultNameSetupViewController(style: .grouped)
        XCTAssertNotNil(vc)
    }
}
