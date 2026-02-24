import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask6F2PTests: XCTestCase {

    // MARK: - Notification names

    func testDidReceiveFileFromURLNotificationExists() {
        let name = Notification.Name.didReceiveFileFromURL
        XCTAssertEqual(name.rawValue, "didReceiveFileFromURL")
    }

    func testDidReceiveFileFromAppleWatchNotificationExists() {
        let name = Notification.Name.didReceiveFileFromAppleWatch
        XCTAssertEqual(name.rawValue, "didReceiveFileFromAppleWatch")
    }

    // MARK: - GPXFilesTableViewController reload support

    func testGPXFilesTableViewControllerRespondsToReloadTableData() {
        let vc = GPXFilesTableViewController()
        let sel = NSSelectorFromString("reloadTableData")
        XCTAssertTrue(vc.responds(to: sel),
                      "GPXFilesTableViewController should have a reloadTableData method")
    }

    // MARK: - ViewController no longer conforms to WCSessionDelegate

    func testViewControllerDoesNotRespondToWCSessionDelegateMethods() {
        let vc = ViewController()
        let sel = NSSelectorFromString("session:didReceiveFile:")
        XCTAssertFalse(vc.responds(to: sel),
                       "ViewController should no longer handle WCSession file transfers directly")
    }
}
