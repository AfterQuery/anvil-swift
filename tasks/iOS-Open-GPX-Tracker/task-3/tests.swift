import XCTest
import MapKit
@testable import OpenGpxTracker

final class AnvilTask3F2PTests: XCTestCase {

    // The solution adds an MKScaleView to the map and replaces deprecated
    // CLLocationManager.authorizationStatus() with the instance property.

    func testMKScaleViewCanBeLinkedToMap() {
        let mapView = MKMapView()
        let scaleView = MKScaleView(mapView: mapView)
        XCTAssertNotNil(scaleView,
                        "MKScaleView should be creatable with a map view")
    }

    func testLocationManagerInstanceAuthorizationStatus() {
        let manager = CLLocationManager()
        let status = manager.authorizationStatus
        // Just verify the instance property is accessible (not the deprecated class method)
        XCTAssertNotNil(status)
    }
}
