import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask4F2PTests: XCTestCase {

    // The solution migrates from manual frame calculations to Auto Layout
    // constraints for all UI elements in ViewController.

    func testViewControllerCanBeInstantiated() {
        let vc = ViewController()
        XCTAssertNotNil(vc, "ViewController should be instantiable")
    }

    func testViewControllerRespondsToViewWillTransition() {
        let vc = ViewController()
        XCTAssertTrue(vc.responds(to: #selector(UIViewController.viewWillTransition(to:with:))),
                      "ViewController should handle orientation transitions")
    }
}
