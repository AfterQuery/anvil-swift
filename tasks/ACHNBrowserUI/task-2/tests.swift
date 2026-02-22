import XCTest
import SwiftUI
@testable import AC_Helper

final class AnvilTask2F2PTests: XCTestCase {
    func testGridStackExists() {
        _ = GridStack<AnyView>(rows: 2, columns: 3) { _, _ in AnyView(EmptyView()) }
    }

    func testGridStackRowsAndColumns() {
        let gs = GridStack<AnyView>(rows: 1, columns: 3) { _, _ in AnyView(EmptyView()) }
        XCTAssertEqual(gs.rows, 1)
        XCTAssertEqual(gs.columns, 3)
    }

    func testGridStackWithSpacing() {
        let gs = GridStack<AnyView>(rows: 2, columns: 3, spacing: 16) { _, _ in AnyView(EmptyView()) }
        XCTAssertEqual(gs.rows, 2)
        XCTAssertEqual(gs.columns, 3)
        XCTAssertEqual(gs.spacing, 16)
    }
}
