import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask8F2PTests: XCTestCase {

    // MARK: - Toast class

    func testToastClassExists() {
        Toast.regular("Test message")
    }

    func testToastInfoExists() {
        Toast.info("Info message")
    }

    func testToastWarningExists() {
        Toast.warning("Warning message")
    }

    func testToastSuccessExists() {
        Toast.success("Success message")
    }

    func testToastErrorExists() {
        Toast.error("Error message")
    }

    func testToastPositionEnum() {
        let _: Toast.Position = .bottom
        let _: Toast.Position = .center
        let _: Toast.Position = .top
    }

    func testToastDelayConstants() {
        XCTAssertGreaterThan(Toast.kDelayShort, 0)
        XCTAssertGreaterThan(Toast.kDelayLong, Toast.kDelayShort,
                             "Long delay should be greater than short delay")
    }

    // MARK: - Toast actually displays

    func testToastRegularAddsViewToWindow() {
        guard let window = UIApplication.shared.windows.first else {
            XCTFail("No window available in test environment")
            return
        }
        let before = window.subviews.count
        Toast.regular("Visibility test")
        let after = window.subviews.count
        XCTAssertGreaterThan(after, before,
                             "Toast.regular should add a subview to the window")
    }

    // MARK: - ToastLabel

    func testToastLabelConvenienceInit() {
        let label = ToastLabel(text: "Hello")
        XCTAssertEqual(label.text, "Hello")
    }

    func testToastLabelHasRoundedCorners() {
        let label = ToastLabel(text: "Test")
        XCTAssertGreaterThan(label.layer.cornerRadius, 0,
                             "ToastLabel should have rounded corners")
    }

    func testToastLabelTextIsCentered() {
        let label = ToastLabel(text: "Test")
        XCTAssertEqual(label.textAlignment, .center,
                       "ToastLabel text should be centered")
    }

    // MARK: - kAppTitle constant

    func testAppTitleConstantExists() {
        XCTAssertFalse(kAppTitle.isEmpty,
                       "kAppTitle should be a non-empty string constant")
    }

    // MARK: - CoreDataAlertView removed (auto-recovery replaces dialog)

    func testCoreDataAlertViewClassRemoved() {
        let alertViewClass = NSClassFromString("OpenGpxTracker.CoreDataAlertView")
        XCTAssertNil(alertViewClass,
                     "CoreDataAlertView should be removed — recovery must be automatic, not dialog-based")
    }

    // MARK: - Session title reflects filename

    func testViewControllerAppTitleLabelReflectsSessionFilename() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let vc = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Could not load ViewController from storyboard")
            return
        }
        vc.loadViewIfNeeded()
        let sessionName = "recovered-session"
        vc.lastGpxFilename = sessionName
        XCTAssertTrue(vc.appTitleLabel.text?.contains(sessionName) == true,
                      "App title label must reflect current session filename when lastGpxFilename is set")
    }
}
