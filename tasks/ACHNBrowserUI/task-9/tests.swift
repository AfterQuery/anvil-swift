import XCTest
@testable import AC_Helper

final class AnvilTask9F2PTests: XCTestCase {

    var collection: UserCollection!

    override func setUp() {
        super.setUp()
        collection = UserCollection()
    }

    // MARK: - TodaySection.SectionName

    func testVillagerVisitsSectionNameExists() {
        // .villagerVisits is a new case added by the patch.
        // This will fail to compile on the base commit.
        let section = TodaySection.SectionName.villagerVisits
        XCTAssertNotNil(section)
    }

    func testVillagerVisitsSectionInDefaults() {
        let defaults = TodaySection.SectionName.allCases
        XCTAssertTrue(
            defaults.contains(.villagerVisits),
            "villagerVisits must be in the default section list"
        )
    }

    // MARK: - UserCollection villager visits

    func testUserCollectionHasVillagerVisitsProperty() {
        // UserCollection.villagerVisits is added by the patch.
        let visits = collection.villagerVisits
        XCTAssertTrue(visits.isEmpty, "villagerVisits should start empty")
    }

    func testToggleVillagerVisitAddsVillager() {
        let villager = Villager.example()
        collection.toggleVillagerVisit(villager: villager)
        XCTAssertTrue(
            collection.villagerVisits.contains(where: { $0.id == villager.id }),
            "Toggling a villager visit should add it to villagerVisits"
        )
    }

    func testToggleVillagerVisitRemovesVillager() {
        let villager = Villager.example()
        collection.toggleVillagerVisit(villager: villager)
        collection.toggleVillagerVisit(villager: villager)
        XCTAssertFalse(
            collection.villagerVisits.contains(where: { $0.id == villager.id }),
            "Toggling a second time should remove the villager"
        )
    }

    func testResetVillagerVisitsClearsAll() {
        let villager = Villager.example()
        collection.toggleVillagerVisit(villager: villager)
        collection.resetVillagerVisits()
        XCTAssertTrue(
            collection.villagerVisits.isEmpty,
            "resetVillagerVisits should clear all visited villagers"
        )
    }

    // MARK: - TodayVillagerVisitsSectionViewModel

    func testShouldShowResetButtonFalseWhenNoneVisited() {
        let vm = TodayVillagerVisitsSectionViewModel()
        XCTAssertFalse(
            vm.shouldShowResetButton,
            "Reset button should be hidden when no villagers have been visited"
        )
    }

    func testShouldShowResetButtonTrueWhenSomeVisited() {
        let villager = Villager.example()
        collection.toggleVillagerVisit(villager: villager)
        let vm = TodayVillagerVisitsSectionViewModel()
        XCTAssertTrue(
            vm.shouldShowResetButton,
            "Reset button should appear when at least one villager has been visited"
        )
    }
}
