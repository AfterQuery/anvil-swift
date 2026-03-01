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
        vc.loadViewIfNeeded()
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

    func testGPXFilesFolderURLPersistsWhenSet() {
        let prefs = Preferences.shared
        let tempDir = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try? FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: tempDir) }

        prefs.gpxFilesFolderURL = tempDir
        XCTAssertEqual(prefs.gpxFilesFolderURL?.path, tempDir.path,
                       "gpxFilesFolderURL must persist when set (for custom output folder)")
        prefs.gpxFilesFolderURL = nil
    }

    func testGPXFileManagerUsesCustomFolderWhenSet() {
        let prefs = Preferences.shared
        let tempDir = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try? FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: tempDir) }
        defer { prefs.gpxFilesFolderURL = nil }

        prefs.gpxFilesFolderURL = tempDir
        XCTAssertEqual(GPXFileManager.GPXFilesFolderURL.path, tempDir.path,
                       "GPXFileManager must use custom folder for saves when gpxFilesFolderURL is set")
    }

    func testGPXFileListAggregatesFromDefaultAndCustomFolders() {
        let prefs = Preferences.shared
        let tempDir = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
        try? FileManager.default.createDirectory(at: tempDir, withIntermediateDirectories: true)
        defer { try? FileManager.default.removeItem(at: tempDir) }
        defer { prefs.gpxFilesFolderURL = nil }

        let testFile = tempDir.appendingPathComponent("aggregation-test.gpx")
        try? "<?xml version=\"1.0\"?><gpx></gpx>".write(to: testFile, atomically: true, encoding: .utf8)

        prefs.gpxFilesFolderURL = tempDir
        let files = GPXFileManager.fileList
        let hasCustomFile = files.contains { $0.fileURL.path.contains("aggregation-test") }
        XCTAssertTrue(hasCustomFile,
                      "File list must include GPX files from custom folder when gpxFilesFolderURL is set")
    }

    func testDocumentPickerDelegateMethodExistsForFolderSelection() {
        let sel = NSSelectorFromString("documentPicker:didPickDocumentsAtURLs:")
        XCTAssertTrue(PreferencesTableViewController.instancesRespond(to: sel),
                      "Must implement documentPicker:didPickDocumentsAtURLs: to handle folder selection")
    }
}
