import XCTest
import UIKit
@testable import Client

@MainActor
final class AnvilTask3F2PTests: XCTestCase {

    func testConstraintReferenceWithNativeConstraint() {
        let constraint = NSLayoutConstraint()
        let ref = ConstraintReference(native: constraint)
        XCTAssertFalse(ref.isUsingSnapKitConstraints)
    }

    func testConstraintReferenceUpdateOffset() {
        let view = UIView()
        let constraint = view.heightAnchor.constraint(equalToConstant: 50)
        let ref = ConstraintReference(native: constraint)
        ref.update(offset: 100)
        XCTAssertEqual(constraint.constant, 100)
    }

    func testConstraintReferenceLayoutConstraint() {
        let constraint = NSLayoutConstraint()
        let ref = ConstraintReference(native: constraint)
        XCTAssertEqual(ref.layoutConstraint, constraint)
    }

    func testBrowserViewControllerLayoutManagerExists() {
        let parent = UIView()
        let header = UIView()
        let manager = BrowserViewControllerLayoutManager(parentView: parent, headerView: header)
        XCTAssertNotNil(manager)
    }
}
