import XCTest
import SwiftUI
@testable import AC_Helper

final class AnvilTask4F2PTests: XCTestCase {
    func testSortEnumExists() {
        let _: VillagersViewModel.Sort = .name
        let _: VillagersViewModel.Sort = .species
    }

    func testSortedVillagersEmptyWithNoData() {
        let vm = VillagersViewModel()
        vm.sort = .name
        XCTAssertTrue(vm.sortedVillagers.isEmpty,
                       "sortedVillagers should be empty when no villagers are loaded")
    }

    func testClearingSortEmptiesSortedVillagers() {
        let vm = VillagersViewModel()
        vm.sort = .name
        vm.sort = nil
        XCTAssertTrue(vm.sortedVillagers.isEmpty,
                       "Clearing sort should empty the sorted villagers array")
    }
}
