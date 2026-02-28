import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask4F2PTests: XCTestCase {

    // MARK: - addConstraints method exists with Bool parameter

    func testViewControllerHasAutoLayoutConstraintsMethod() {
        let _: (ViewController) -> (Bool) -> Void = { $0.addConstraints }
    }

    func testAddConstraintsIncreasesConstraintCount() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let vc = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Could not load ViewController from storyboard")
            return
        }
        vc.loadViewIfNeeded()
        let allConstraintsBefore = countActiveConstraints(in: vc.view)
        vc.addConstraints(false)
        let allConstraintsAfter = countActiveConstraints(in: vc.view)
        XCTAssertGreaterThan(allConstraintsAfter, allConstraintsBefore,
                             "addConstraints(_:) must actually add layout constraints")
    }

    func testAutoLayoutDisablesAutoresizingOnMultipleSubviews() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let vc = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Could not load ViewController from storyboard")
            return
        }
        vc.loadViewIfNeeded()
        vc.addConstraints(false)
        let constrainedSubviews = vc.view.subviews.filter { !$0.translatesAutoresizingMaskIntoConstraints }
        XCTAssertGreaterThanOrEqual(constrainedSubviews.count, 2,
                                    "Multiple subviews should use Auto Layout after addConstraints(_:)")
    }

    func testAddConstraintsAddsSubstantialLayout() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let vc = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Could not load ViewController from storyboard")
            return
        }
        vc.loadViewIfNeeded()
        let before = countActiveConstraints(in: vc.view)
        vc.addConstraints(false)
        let after = countActiveConstraints(in: vc.view)
        XCTAssertGreaterThanOrEqual(after - before, 5,
                                    "addConstraints(_:) must add enough constraints for proper layout (buttons, compass, labels)")
    }

    // MARK: - Helpers

    private func countActiveConstraints(in view: UIView) -> Int {
        var count = view.constraints.count
        for subview in view.subviews {
            count += subview.constraints.count
        }
        return count
    }
}
