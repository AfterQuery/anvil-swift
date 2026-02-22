import XCTest
import SwiftUI
@testable import AC_Helper
import Backend

final class AnvilTask1F2PTests: XCTestCase {

    // MARK: - Backend: core new method

    func testIsActiveAtThisHourReturnsFalseWithoutActiveMonths() {
        let json = """
        {"name":"Test","category":"Fish","filename":"test"}
        """
        let item = try! JSONDecoder().decode(Item.self, from: json.data(using: .utf8)!)
        XCTAssertFalse(item.isActiveAtThisHour(),
                       "Item without active hours data should not be active this hour")
    }

    // MARK: - App ViewModel: CritterInfo integration point

    func testCritterInfoHasToCatchNowAndToCatchLater() {
        let info = ActiveCrittersViewModel.CritterInfo(
            new: [], leaving: [], caught: [],
            toCatchNow: [], toCatchLater: []
        )
        XCTAssertTrue(info.toCatchNow.isEmpty)
        XCTAssertTrue(info.toCatchLater.isEmpty)
    }

    func testCritterInfoStoresNowAndLaterItems() {
        let json = """
        {"name":"TestFish","category":"Fish","filename":"test_fish"}
        """
        let item = try! JSONDecoder().decode(Item.self, from: json.data(using: .utf8)!)

        let info = ActiveCrittersViewModel.CritterInfo(
            new: [], leaving: [], caught: [],
            toCatchNow: [item], toCatchLater: []
        )
        XCTAssertEqual(info.toCatchNow.count, 1)
        XCTAssertTrue(info.toCatchLater.isEmpty)
    }
}
