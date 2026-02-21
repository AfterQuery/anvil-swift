import XCTest
@testable import Backend

final class AnvilTask1Tests: XCTestCase {

    // MARK: - isActiveThisMonth (renamed from isActive)

    func testIsActiveThisMonthReturnsFalseWithoutActiveMonths() {
        let json = """
        {"name":"Test","category":"Fish","filename":"test"}
        """
        let item = try! JSONDecoder().decode(Item.self, from: json.data(using: .utf8)!)
        XCTAssertFalse(item.isActiveThisMonth(),
                       "Item without activeMonths data should not be active this month")
    }

    // MARK: - isActiveAtThisHour

    func testIsActiveAtThisHourReturnsFalseWithoutActiveMonths() {
        let json = """
        {"name":"Test","category":"Fish","filename":"test"}
        """
        let item = try! JSONDecoder().decode(Item.self, from: json.data(using: .utf8)!)
        XCTAssertFalse(item.isActiveAtThisHour(),
                       "Item without active hours data should not be active this hour")
    }

    // MARK: - filterActiveThisMonth

    func testFilterActiveThisMonthExcludesInactiveItems() {
        let json = """
        {"name":"Test","category":"Fish","filename":"test"}
        """
        let item = try! JSONDecoder().decode(Item.self, from: json.data(using: .utf8)!)
        let result = [item].filterActiveThisMonth()
        XCTAssertTrue(result.isEmpty,
                      "Item without active months should be excluded by filterActiveThisMonth")
    }

    // MARK: - formattedTimes

    func testFormattedTimesReturnsNilWithoutActiveMonths() {
        let json = """
        {"name":"Test","category":"Fish","filename":"test"}
        """
        let item = try! JSONDecoder().decode(Item.self, from: json.data(using: .utf8)!)
        XCTAssertNil(item.formattedTimes(),
                     "formattedTimes should return nil without active month data")
    }
}
