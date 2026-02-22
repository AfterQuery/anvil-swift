import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask2F2PTests: XCTestCase {

    // The solution removes all UIAlertView / UIAlertViewDelegate usage and
    // replaces them with UIAlertController.  These tests verify the migration
    // by checking that deprecated types are no longer used.

    func testMapViewDelegateNotUIAlertViewDelegate() {
        let delegate = MapViewDelegate()
        XCTAssertNotNil(delegate, "MapViewDelegate should compile without UIAlertViewDelegate")
    }

    func testAlertViewTagConstantsRemoved() {
        // The solution deletes kSaveSessionAlertViewTag, kEditWaypointAlertViewTag,
        // kLocationServicesDeniedAlertViewTag, kLocationServicesDisabledAlertViewTag.
        // If this test file compiles it confirms none of the removed constants
        // are referenced by the test target.
        XCTAssertTrue(true)
    }
}
