import XCTest
import MapKit
@testable import OpenGpxTracker

final class AnvilTask3F2PTests: XCTestCase {

    // MARK: - scaleBar property type

    func testViewControllerHasScaleBarProperty() {
        let _: KeyPath<ViewController, MKScaleView> = \.scaleBar
    }

    // MARK: - Storyboard integration

    func testViewControllerLoadableFromStoryboardWithScaleBar() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let viewController = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Initial view controller is not ViewController")
            return
        }
        viewController.loadViewIfNeeded()
        XCTAssertNotNil(viewController.scaleBar,
                        "scaleBar should be initialised after view loads")
    }

    func testScaleBarIsInViewHierarchy() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let viewController = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Initial view controller is not ViewController")
            return
        }
        viewController.loadViewIfNeeded()
        XCTAssertTrue(viewController.scaleBar.isDescendant(of: viewController.view),
                      "scaleBar should be added to the view hierarchy")
    }

    func testScaleBarIsLinkedToMap() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let viewController = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Initial view controller is not ViewController")
            return
        }
        viewController.loadViewIfNeeded()
        let scaleBar = viewController.scaleBar
        XCTAssertNotNil(scaleBar.mapView,
                        "scaleBar must be linked to a map view so it updates with zoom")
    }

    func testScaleBarUsesAutoLayout() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let viewController = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Initial view controller is not ViewController")
            return
        }
        viewController.loadViewIfNeeded()
        XCTAssertFalse(viewController.scaleBar.translatesAutoresizingMaskIntoConstraints,
                       "scaleBar should use Auto Layout (translatesAutoresizingMaskIntoConstraints = false)")
    }

    func testScaleBarIsLinkedToSameMapAsViewController() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let viewController = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Initial view controller is not ViewController")
            return
        }
        viewController.loadViewIfNeeded()
        XCTAssertTrue(viewController.scaleBar.mapView === viewController.map,
                      "scaleBar must be linked to the ViewController's map so it updates with zoom")
    }
}
