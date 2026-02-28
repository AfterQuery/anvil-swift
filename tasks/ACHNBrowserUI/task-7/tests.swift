import XCTest
import SwiftUI
@testable import ACHNBrowserUI

final class AnvilTask7F2PTests: XCTestCase {

    // MARK: - TurnipsViewModel

    func testTurnipsViewModelDefaultIslands() {
        let vm = TurnipsViewModel()
        XCTAssertNil(vm.islands, "Islands should default to nil before fetching")
    }

    func testTurnipsViewModelHasFetchMethod() {
        let vm = TurnipsViewModel()
        let _: () -> Void = vm.fetch
    }

    func testTurnipsViewModelIsObservableObject() {
        let vm = TurnipsViewModel()
        XCTAssertNotNil(vm.objectWillChange,
                        "TurnipsViewModel must conform to ObservableObject")
    }

    // MARK: - Tab structure

    func testTabbarViewHasTurnipsTab() {
        let allTabs: [TabbarView.Tab] = [.items, .wardrobe, .nature, .villagers, .collection, .turnips]
        XCTAssertTrue(allTabs.contains(.turnips),
                      "Turnips should be present in the tab enum")
    }

    // MARK: - Island model

    func testIslandConformsToIdentifiable() {
        func requireIdentifiable<T: Identifiable>(_: T.Type) {}
        requireIdentifiable(Island.self)
    }

    func testIslandDescriptionIsOptional() {
        let mirror = Mirror(reflecting: Island.self)
        _ = mirror
        let keyPath: KeyPath<Island, String?> = \Island.islandDescription
        XCTAssertNotNil(keyPath, "islandDescription must be Optional<String>")
    }

    // MARK: - CategoriesView (no binding, drill-down navigation)

    func testCategoriesViewInitWithoutBinding() {
        let _ = CategoriesView(categories: Categories.items())
    }

    // MARK: - CategoryDetailView

    func testCategoryDetailViewAcceptsCategories() {
        let _ = CategoryDetailView(categories: Categories.wardrobe())
    }

    func testCategoryDetailViewWithNature() {
        let _ = CategoryDetailView(categories: Categories.nature())
    }

    func testCategoryDetailViewWithItems() {
        let _ = CategoryDetailView(categories: Categories.items())
    }

    // MARK: - ItemsListView accepts external view model

    func testItemsListViewAcceptsViewModel() {
        let vm = ItemsViewModel(categorie: .housewares)
        let _ = ItemsListView(viewModel: vm)
    }

    func testItemsViewModelInitIsPublic() {
        let vm = ItemsViewModel(categorie: .fossils)
        XCTAssertNotNil(vm)
    }
}
