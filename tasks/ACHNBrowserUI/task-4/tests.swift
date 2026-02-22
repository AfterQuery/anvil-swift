import XCTest
import SwiftUI
@testable import AC_Helper
import Backend

final class AnvilTask4F2PTests: XCTestCase {

    // MARK: - Helpers

    private func makeVillager(id: Int, name: String, species: String) -> Villager {
        let json = """
        {"id":\(id),"name":{"name-en":"\(name)"},"personality":"Normal","gender":"Female","species":"\(species)"}
        """
        return try! JSONDecoder().decode(Villager.self, from: json.data(using: .utf8)!)
    }

    // MARK: - Structural

    func testSortEnumExists() {
        let _: VillagersViewModel.Sort = .name
        let _: VillagersViewModel.Sort = .species
    }

    func testSortDefaultsToNil() {
        let vm = VillagersViewModel()
        XCTAssertNil(vm.sort, "Sort should default to nil")
        XCTAssertTrue(vm.sortedVillagers.isEmpty)
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

    // MARK: - Behavioral

    func testSortByNameProducesAlphabeticalOrder() {
        let vm = VillagersViewModel()
        vm.villagers = [
            makeVillager(id: 1, name: "Zucker", species: "Octopus"),
            makeVillager(id: 2, name: "Apollo", species: "Eagle"),
            makeVillager(id: 3, name: "Marina", species: "Octopus"),
        ]
        vm.sort = .name
        XCTAssertEqual(vm.sortedVillagers.count, 3)
        XCTAssertEqual(vm.sortedVillagers.first?.localizedName, "Apollo")
        XCTAssertEqual(vm.sortedVillagers.last?.localizedName, "Zucker")
    }

    func testSortBySpeciesProducesAlphabeticalOrder() {
        let vm = VillagersViewModel()
        vm.villagers = [
            makeVillager(id: 1, name: "Zucker", species: "Octopus"),
            makeVillager(id: 2, name: "Apollo", species: "Eagle"),
        ]
        vm.sort = .species
        XCTAssertEqual(vm.sortedVillagers.count, 2)
        XCTAssertEqual(vm.sortedVillagers.first?.species, "Eagle")
        XCTAssertEqual(vm.sortedVillagers.last?.species, "Octopus")
    }

    func testSortReversalOnRepeat() {
        let vm = VillagersViewModel()
        vm.villagers = [
            makeVillager(id: 1, name: "Zucker", species: "Octopus"),
            makeVillager(id: 2, name: "Apollo", species: "Eagle"),
        ]
        vm.sort = .name
        XCTAssertEqual(vm.sortedVillagers.first?.localizedName, "Apollo",
                       "First sort should be ascending")

        vm.sort = .name
        XCTAssertEqual(vm.sortedVillagers.first?.localizedName, "Zucker",
                       "Repeating the same sort should reverse to descending")
    }
}
