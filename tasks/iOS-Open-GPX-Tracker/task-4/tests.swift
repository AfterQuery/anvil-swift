import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask4F2PTests: XCTestCase {

    func testViewControllerHasStoryboardIdentifier() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        let vc = storyboard.instantiateViewController(withIdentifier: "RootViewController")
        XCTAssertTrue(vc is ViewController,
                      "ViewController should be instantiable from storyboard with identifier 'RootViewController'")
    }
}
