import XCTest
@testable import AC_Helper

final class AnvilTask4F2PTests: XCTestCase {
    func testSortEnumExists() {
        let _: VillagersViewModel.Sort = .name
        let _: VillagersViewModel.Sort = .species
    }

    func testSortedVillagersProperty() {
        let vm = VillagersViewModel()
        vm.sort = .name
        XCTAssertNotNil(vm.sortedVillagers)
    }
}
