import XCTest
import MapKit
@testable import OpenGpxTracker

final class AnvilTask3F2PTests: XCTestCase {

    func testViewControllerHasScaleBarProperty() {
        let vc = ViewController()
        let scaleBar: MKScaleView = vc.scaleBar
        XCTAssertNotNil(scaleBar,
                        "ViewController should have an MKScaleView scaleBar property")
    }
}
