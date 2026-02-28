import XCTest
import UIKit
import WatchConnectivity
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

    func testNotificationNamesAreDistinct() {
        XCTAssertNotEqual(Notification.Name.didReceiveFileFromURL,
                          Notification.Name.didReceiveFileFromAppleWatch,
                          "The two notification names must be different")
    }

    // MARK: - GPXFilesTableViewController reload support

    func testGPXFilesTableViewControllerRespondsToReloadTableData() {
        let sel = NSSelectorFromString("reloadTableData")
        XCTAssertTrue(GPXFilesTableViewController.instancesRespond(to: sel),
                      "GPXFilesTableViewController should have a reloadTableData method")
    }

    func testFileTableViewControllerReloadsOnURLNotification() {
        let vc = GPXFilesTableViewController()
        vc.loadViewIfNeeded()
        let expectation = XCTNSNotificationExpectation(
            name: .didReceiveFileFromURL,
            object: nil
        )
        NotificationCenter.default.post(name: .didReceiveFileFromURL, object: nil)
        wait(for: [expectation], timeout: 2.0)
    }

    func testFileTableViewControllerReloadsOnAppleWatchNotification() {
        let vc = GPXFilesTableViewController()
        vc.loadViewIfNeeded()
        let expectation = XCTNSNotificationExpectation(
            name: .didReceiveFileFromAppleWatch,
            object: nil
        )
        NotificationCenter.default.post(name: .didReceiveFileFromAppleWatch, object: nil)
        wait(for: [expectation], timeout: 2.0)
    }

    func testReloadTableDataIsCalledWhenURLNotificationFires() {
        class SpyVC: GPXFilesTableViewController {
            var reloadTableDataCalled = false
            @objc override func reloadTableData() {
                reloadTableDataCalled = true
                super.reloadTableData()
            }
        }
        let vc = SpyVC()
        vc.loadViewIfNeeded()
        NotificationCenter.default.post(name: .didReceiveFileFromURL, object: nil)
        RunLoop.current.run(until: Date().addingTimeInterval(0.1))
        XCTAssertTrue(vc.reloadTableDataCalled,
                      "GPXFilesTableViewController must observe didReceiveFileFromURL and call reloadTableData")
    }

    func testReloadTableDataIsCalledWhenAppleWatchNotificationFires() {
        class SpyVC: GPXFilesTableViewController {
            var reloadTableDataCalled = false
            @objc override func reloadTableData() {
                reloadTableDataCalled = true
                super.reloadTableData()
            }
        }
        let vc = SpyVC()
        vc.loadViewIfNeeded()
        NotificationCenter.default.post(name: .didReceiveFileFromAppleWatch, object: nil)
        RunLoop.current.run(until: Date().addingTimeInterval(0.1))
        XCTAssertTrue(vc.reloadTableDataCalled,
                      "GPXFilesTableViewController must observe didReceiveFileFromAppleWatch and call reloadTableData")
    }

    // MARK: - WCSession delegation moved to AppDelegate

    func testViewControllerDoesNotRespondToWCSessionDelegateMethods() {
        let sel = NSSelectorFromString("session:didReceiveFile:")
        XCTAssertFalse(ViewController.instancesRespond(to: sel),
                       "ViewController should no longer handle WCSession file transfers directly")
    }

    func testAppDelegateConformsToWCSessionDelegate() {
        let appDelegate = AppDelegate()
        XCTAssertTrue(appDelegate is WCSessionDelegate,
                      "AppDelegate should conform to WCSessionDelegate to handle file transfers")
    }

    func testAppDelegateRespondsToDidReceiveFile() {
        let sel = NSSelectorFromString("session:didReceiveFile:")
        XCTAssertTrue(AppDelegate.instancesRespond(to: sel),
                      "AppDelegate should implement session(_:didReceive:) for Apple Watch file transfers")
    }
}
