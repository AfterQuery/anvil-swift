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
        XCTAssertEqual(Toast.kDelayShort, 2.0)
        XCTAssertEqual(Toast.kDelayLong, 5.0)
    }

    // MARK: - ToastLabel

    func testToastLabelConvenienceInit() {
        let label = ToastLabel(text: "Hello")
        XCTAssertEqual(label.text, "Hello")
    }

    // MARK: - kAppTitle constant

    func testAppTitleConstantExists() {
        XCTAssertFalse(kAppTitle.isEmpty,
                       "kAppTitle should be a non-empty string constant")
    }
}
