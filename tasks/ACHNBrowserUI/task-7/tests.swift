import XCTest
import SwiftUI
@testable import AC_Helper

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
        let tab: TabbarView.Tab = .turnips
        XCTAssertEqual(tab.rawValue, TabbarView.Tab.turnips.rawValue)
    }

    // MARK: - Island Identifiable conformance

    func testIslandConformsToIdentifiable() {
        func requireIdentifiable<T: Identifiable>(_: T.Type) {}
        requireIdentifiable(Island.self)
    }

    // MARK: - CategoriesView

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

    // MARK: - ItemsListView accepts external view model

    func testItemsListViewAcceptsViewModel() {
        let vm = ItemsViewModel(categorie: .housewares)
        let _ = ItemsListView(viewModel: vm)
    }
}
