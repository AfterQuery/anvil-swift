import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask4F2PTests: XCTestCase {

    // MARK: - addConstraints method exists with Bool parameter

    func testViewControllerHasAutoLayoutConstraintsMethod() {
        let _: (ViewController) -> (Bool) -> Void = { $0.addConstraints }
    }

    func testAddConstraintsProducesLayoutConstraints() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let vc = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Could not load ViewController from storyboard")
            return
        }
        vc.loadViewIfNeeded()
        vc.addConstraints(false)
        XCTAssertFalse(vc.view.constraints.isEmpty,
                       "View should have Auto Layout constraints after addConstraints(_:) is called")
    }

    func testAutoLayoutDisablesAutoresizingOnSubviews() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let vc = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Could not load ViewController from storyboard")
            return
        }
        vc.loadViewIfNeeded()
        vc.addConstraints(false)
        let constrainedSubviews = vc.view.subviews.filter { !$0.translatesAutoresizingMaskIntoConstraints }
        XCTAssertGreaterThan(constrainedSubviews.count, 0,
                             "At least some subviews should have translatesAutoresizingMaskIntoConstraints = false")
    }
}
