import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask2F2PTests: XCTestCase {

    func testMapViewDelegateNoLongerImplementsAlertViewCallback() {
        let delegate = MapViewDelegate()
        let sel = NSSelectorFromString("alertView:clickedButtonAtIndex:")
        XCTAssertFalse(delegate.responds(to: sel),
                       "MapViewDelegate should not implement UIAlertViewDelegate methods after migration")
    }

    func testViewControllerNoLongerImplementsAlertViewCallback() {
        let vc = ViewController()
        let sel = NSSelectorFromString("alertView:clickedButtonAtIndex:")
        XCTAssertFalse(vc.responds(to: sel),
                       "ViewController should not implement UIAlertViewDelegate methods after migration")
    }
}
