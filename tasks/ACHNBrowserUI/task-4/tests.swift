import XCTest
@testable import Backend

final class AnvilTask4P2PTests: XCTestCase {

    func testVillagerLocalizedNameExists() {
        let v = static_villager
        XCTAssertFalse(v.localizedName.isEmpty,
                       "Villager should have a non-empty localizedName")
    }

    func testVillagerSpeciesExists() {
        let v = static_villager
        XCTAssertFalse(v.species.isEmpty,
                       "Villager should have a non-empty species")
    }

    func testVillagerNameSortingUsingLocalizedCompare() {
        let a = Villager(id: 1, fileName: "a", catchPhrase: nil,
                         name: ["name-en": "Bob"], personality: "Lazy",
                         birthday: nil, gender: "Male", species: "Cat")
        let b = Villager(id: 2, fileName: "b", catchPhrase: nil,
                         name: ["name-en": "Alice"], personality: "Normal",
                         birthday: nil, gender: "Female", species: "Dog")

        let sorted = [a, b].sorted {
            $0.localizedName.localizedCompare($1.localizedName) == .orderedAscending
        }
        XCTAssertEqual(sorted.first?.localizedName, "Alice")
        XCTAssertEqual(sorted.last?.localizedName, "Bob")
    }
}
