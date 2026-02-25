import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask10F2PTests: XCTestCase {

    // MARK: - Preferences: gpxFilesFolderURL

    func testGPXFilesFolderDefaultsKeyExists() {
        XCTAssertFalse(kDefaultsKeyGPXFilesFolder.isEmpty,
                       "UserDefaults key for GPX files folder should be a non-empty string")
    }

    func testGPXFilesFolderURLDefaultsToNil() {
        let prefs = Preferences.shared
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
        XCTAssertGreaterThanOrEqual(kGPXFilesLocationSection, 0,
                                    "GPX files location section should be a valid section index")
    }

    func testSectionCountIncludesGPXFilesLocation() {
        let vc = PreferencesTableViewController(style: .grouped)
        let sections = vc.numberOfSections(in: vc.tableView)
        XCTAssertGreaterThanOrEqual(sections, 6,
                                    "Preferences should have at least 6 sections after adding GPX files location")
    }

    // MARK: - UIDocumentPickerDelegate conformance

    func testPreferencesConformsToDocumentPickerDelegate() {
        let vc = PreferencesTableViewController(style: .grouped)
        XCTAssertTrue(vc is UIDocumentPickerDelegate,
                      "PreferencesTableViewController should conform to UIDocumentPickerDelegate")
    }
}
