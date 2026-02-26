import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask2F2PTests: XCTestCase {

    // MARK: - UIAlertViewDelegate conformance removed

    func testMapViewDelegateDoesNotConformToUIAlertViewDelegate() {
        guard let proto = NSProtocolFromString("UIAlertViewDelegate") else { return }
        XCTAssertFalse(MapViewDelegate.conforms(to: proto),
                       "MapViewDelegate should no longer declare UIAlertViewDelegate conformance")
    }

    func testViewControllerDoesNotConformToUIAlertViewDelegate() {
        guard let proto = NSProtocolFromString("UIAlertViewDelegate") else { return }
        XCTAssertFalse(ViewController.conforms(to: proto),
                       "ViewController should no longer declare UIAlertViewDelegate conformance")
    }

    // MARK: - UIAlertViewDelegate callback methods removed

    func testMapViewDelegateNoLongerImplementsAlertViewCallback() {
        let sel = NSSelectorFromString("alertView:clickedButtonAtIndex:")
        XCTAssertFalse(MapViewDelegate.instancesRespond(to: sel),
                       "MapViewDelegate should not implement UIAlertViewDelegate methods after migration")
    }

    func testViewControllerNoLongerImplementsAlertViewCallback() {
        let sel = NSSelectorFromString("alertView:clickedButtonAtIndex:")
        XCTAssertFalse(ViewController.instancesRespond(to: sel),
                       "ViewController should not implement UIAlertViewDelegate methods after migration")
    }

    // MARK: - Alert presentation methods still functional after migration

    func testViewControllerLoadsAfterMigration() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let vc = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("ViewController should still load from storyboard after migration")
            return
        }
        vc.loadViewIfNeeded()
        XCTAssertNotNil(vc.view, "ViewController view should load without UIAlertViewDelegate")
    }

    func testMapViewDelegateCanBeInstantiated() {
        let delegate = MapViewDelegate()
        XCTAssertNotNil(delegate)
    }

    func testMapViewDelegateStillHandlesCalloutAccessory() {
        let sel = NSSelectorFromString("mapView:annotationView:calloutAccessoryControlTapped:")
        XCTAssertTrue(MapViewDelegate.instancesRespond(to: sel),
                      "MapViewDelegate should still handle callout accessory taps after migration")
    }
}
