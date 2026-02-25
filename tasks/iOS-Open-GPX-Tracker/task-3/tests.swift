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
        let vc = storyboard.instantiateViewController(withIdentifier: "RootViewController")
        guard let viewController = vc as? ViewController else {
            XCTFail("Initial view controller is not ViewController")
            return
        }
        viewController.loadViewIfNeeded()
        XCTAssertNotNil(viewController.scaleBar,
                        "scaleBar should be initialised after view loads")
    }

    func testScaleBarIsInViewHierarchy() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        let vc = storyboard.instantiateViewController(withIdentifier: "RootViewController")
        guard let viewController = vc as? ViewController else {
            XCTFail("Initial view controller is not ViewController")
            return
        }
        viewController.loadViewIfNeeded()
        XCTAssertTrue(viewController.scaleBar.isDescendant(of: viewController.view),
                      "scaleBar should be added to the view hierarchy")
    }
}
