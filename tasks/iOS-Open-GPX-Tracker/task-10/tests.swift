import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask10F2PTests: XCTestCase {

    // MARK: - Preferences: gpxFilesFolderURL

    func testGPXFilesFolderDefaultsKeyExists() {
        XCTAssertEqual(kDefaultsKeyGPXFilesFolder, "GPXFilesFolder",
                       "UserDefaults key for GPX files folder should be 'GPXFilesFolder'")
    }

    func testGPXFilesFolderURLDefaultsToNil() {
        let prefs = Preferences.shared
        // Clear any previously stored bookmark
        UserDefaults.standard.removeObject(forKey: kDefaultsKeyGPXFilesFolder)
        XCTAssertNil(prefs.gpxFilesFolderURL,
                     "gpxFilesFolderURL should be nil when no custom folder is set")
    }

    func testGPXFilesFolderURLCanBeSetToNil() {
        let prefs = Preferences.shared
        prefs.gpxFilesFolderURL = nil
        XCTAssertNil(prefs.gpxFilesFolderURL)
    }

    // MARK: - Preferences table section constants

    func testGPXFilesLocationSectionExists() {
        XCTAssertEqual(kGPXFilesLocationSection, 5,
                       "GPX files location section should be at index 5")
    }

    func testSectionCountIncreasedTo6() {
        let vc = PreferencesTableViewController(style: .grouped)
        let sections = vc.numberOfSections(in: vc.tableView)
        XCTAssertEqual(sections, 6,
                       "Preferences should have 6 sections after adding GPX files location")
    }

    // MARK: - UIDocumentPickerDelegate conformance

    func testPreferencesConformsToDocumentPickerDelegate() {
        let vc = PreferencesTableViewController(style: .grouped)
        XCTAssertTrue(vc is UIDocumentPickerDelegate,
                      "PreferencesTableViewController should conform to UIDocumentPickerDelegate")
    }
}
