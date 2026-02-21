import XCTest
@testable import Backend

final class AnvilTask2Tests: XCTestCase {

    // Task 2 replaces per-row turnip price views with a unified GridStack layout.
    // All changes are in the app target (TurnipsView, GridStack); no Backend code
    // is modified.  These tests verify the Backend package still compiles and that
    // turnip-related model helpers the view depends on remain intact.

    func testArrayAverageExtension() {
        let prices = [80, 100, 120]
        let avg = prices.average
        XCTAssertEqual(avg, 100.0, accuracy: 0.01,
                       "Array<Int>.average should compute the arithmetic mean")
    }

    func testEmptyArrayAverageIsZero() {
        let empty: [Int] = []
        XCTAssertEqual(empty.average, 0.0, accuracy: 0.01)
    }
}
