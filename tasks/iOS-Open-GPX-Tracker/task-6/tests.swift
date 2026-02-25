import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask6F2PTests: XCTestCase {

    // MARK: - Notification names

    func testDidReceiveFileFromURLNotificationExists() {
        let name = Notification.Name.didReceiveFileFromURL
        XCTAssertFalse(name.rawValue.isEmpty,
                       "didReceiveFileFromURL notification should have a non-empty rawValue")
    }

    func testDidReceiveFileFromAppleWatchNotificationExists() {
        let name = Notification.Name.didReceiveFileFromAppleWatch
        XCTAssertFalse(name.rawValue.isEmpty,
                       "didReceiveFileFromAppleWatch notification should have a non-empty rawValue")
    }

    // MARK: - GPXFilesTableViewController reload support

    func testGPXFilesTableViewControllerRespondsToReloadTableData() {
        let sel = NSSelectorFromString("reloadTableData")
        XCTAssertTrue(GPXFilesTableViewController.instancesRespond(to: sel),
                      "GPXFilesTableViewController should have a reloadTableData method")
    }

    // MARK: - ViewController no longer conforms to WCSessionDelegate

    func testViewControllerDoesNotRespondToWCSessionDelegateMethods() {
        let sel = NSSelectorFromString("session:didReceiveFile:")
        XCTAssertFalse(ViewController.instancesRespond(to: sel),
                       "ViewController should no longer handle WCSession file transfers directly")
    }
}
