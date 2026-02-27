import XCTest
import SwiftUI
@testable import AC_Helper

final class AnvilTask2F2PTests: XCTestCase {

    // MARK: - GridStack struct basics

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

    func testGridStackDefaultSpacingIsNil() {
        let gs = GridStack<AnyView>(rows: 2, columns: 3) { _, _ in AnyView(EmptyView()) }
        XCTAssertNil(gs.spacing,
                     "GridStack without explicit spacing should default to nil")
    }

    // MARK: - GridStack content closure

    func testGridStackContentClosureReceivesCorrectIndices() {
        var receivedIndices: [(Int, Int)] = []
        let gs = GridStack<AnyView>(rows: 2, columns: 3) { row, col in
            receivedIndices.append((row, col))
            return AnyView(Text("cell"))
        }
        for row in 0..<2 {
            for col in 0..<3 {
                _ = gs.content(row, col)
            }
        }
        XCTAssertEqual(receivedIndices.count, 6)
        XCTAssertTrue(receivedIndices.contains(where: { $0.0 == 0 && $0.1 == 0 }))
        XCTAssertTrue(receivedIndices.contains(where: { $0.0 == 1 && $0.1 == 2 }))
    }

    // MARK: - GridStack is a real View (not just a struct)

    func testGridStackConformsToView() {
        let gs = GridStack<AnyView>(rows: 2, columns: 2) { _, _ in AnyView(Text("cell")) }
        let body = gs.body
        XCTAssertNotNil(body, "GridStack.body must produce a View")
    }

    // MARK: - GridStack ViewBuilder closure

    func testGridStackUsesViewBuilderContent() {
        let gs = GridStack(rows: 1, columns: 2, spacing: 8) { row, col in
            Text("R\(row)C\(col)")
        }
        XCTAssertEqual(gs.rows, 1)
        XCTAssertEqual(gs.columns, 2)
        XCTAssertEqual(gs.spacing, 8)
    }
}
