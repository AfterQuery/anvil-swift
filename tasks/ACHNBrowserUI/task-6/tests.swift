import XCTest
import SwiftUI
import Combine
@testable import AC_Helper
import Backend

final class AnvilTask6F2PTests: XCTestCase {

    // MARK: - DashboardViewModel existence and ObservableObject

    func testDashboardViewModelIsObservableObject() {
        let vm = DashboardViewModel()
        XCTAssertNotNil(vm.objectWillChange,
                        "DashboardViewModel must conform to ObservableObject")
    }

    func testDashboardViewModelDefaultState() {
        let vm = DashboardViewModel()
        XCTAssertNil(vm.recentListings, "recentListings should default to nil")
        XCTAssertNil(vm.island, "island should default to nil")
        XCTAssertTrue(vm.fishes.isEmpty, "fishes should default to empty")
        XCTAssertTrue(vm.bugs.isEmpty, "bugs should default to empty")
        XCTAssertTrue(vm.fossils.isEmpty, "fossils should default to empty")
    }

    func testDashboardViewModelHasFetchMethods() {
        let vm = DashboardViewModel()
        let _: () -> Void = vm.fetchListings
        let _: () -> Void = vm.fetchIsland
        let _: () -> Void = vm.fetchCritters
    }

    // MARK: - Tab structure: dashboard is first/default

    func testTabbarViewHasDashboardTab() {
        let tab: TabbarView.Tab = .dashboard
        XCTAssertEqual(tab.rawValue, 0,
                       "Dashboard should be the first tab (rawValue 0)")
    }

    // MARK: - Categories helper methods

    func testCategoriesFishMethod() {
        let fish = Categories.fish()
        XCTAssertTrue(fish == .fishesNorth || fish == .fishesSouth,
                      "Categories.fish() must return a fish category for the current hemisphere")
    }

    func testCategoriesBugsMethod() {
        let bugs = Categories.bugs()
        XCTAssertTrue(bugs == .bugsNorth || bugs == .bugsSouth,
                      "Categories.bugs() must return a bugs category for the current hemisphere")
    }

    // MARK: - Listing model additions

    func testListingHasNameProperty() throws {
        let json = """
        {"id":"1","itemId":"100","amount":1,"active":true,"selling":true,"needMaterials":false,"username":"test","name":"Chair","img":"https://example.com/img.png"}
        """
        let listing = try JSONDecoder().decode(Listing.self, from: json.data(using: .utf8)!)
        XCTAssertEqual(listing.name, "Chair")
        XCTAssertNotNil(listing.img)
    }

    func testListingNameIsOptional() throws {
        let json = """
        {"id":"2","itemId":"200","amount":1,"active":true,"selling":true,"needMaterials":false,"username":"test"}
        """
        let listing = try JSONDecoder().decode(Listing.self, from: json.data(using: .utf8)!)
        XCTAssertNil(listing.name, "name should be nil when not present")
        XCTAssertNil(listing.img, "img should be nil when not present")
    }

    // MARK: - NookazonService.recentListings

    func testNookazonServiceHasRecentListingsMethod() {
        let _: AnyPublisher<[Listing], Error> = NookazonService.recentListings()
    }
}
