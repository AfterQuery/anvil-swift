import XCTest
@testable import Client

// Extends MockTabManager so getTabForUUID returns a real tab, enabling
// save/restore behavioral tests without reaching into private internals.
private class HomepageScrollTabManager: MockTabManager {
    private var tabsByUUID: [String: Tab] = [:]

    func registerTab(_ tab: Tab) {
        tabsByUUID[tab.tabUUID] = tab
        tabs.append(tab)
        selectedTab = tab
    }

    override func getTabForUUID(uuid: String) -> Tab? {
        return tabsByUUID[uuid]
    }
}

@MainActor
final class AnvilTask4F2PTests: XCTestCase {

    override func setUp() async throws {
        try await super.setUp()
        DependencyHelperMock().bootstrapDependencies()
        LegacyFeatureFlagsManager.shared.initializeDeveloperFeatures(with: MockProfile())
    }

    override func tearDown() async throws {
        DependencyHelperMock().reset()
        try await super.tearDown()
    }

    // Tab property: starts nil, can be set independently per tab instance
    func testTabHasHomepageScrollOffsetProperty() {
        let tab = MockTab(profile: MockProfile(), windowUUID: .XCTestDefaultUUID)
        XCTAssertNil(tab.homepageScrollOffset)
        tab.homepageScrollOffset = 150.0
        XCTAssertEqual(tab.homepageScrollOffset, 150.0)
    }

    // Each tab stores its own independent scroll offset
    func testScrollOffsetIsIndependentPerTab() {
        let tab1 = MockTab(profile: MockProfile(), windowUUID: .XCTestDefaultUUID)
        let tab2 = MockTab(profile: MockProfile(), windowUUID: .XCTestDefaultUUID)
        tab1.homepageScrollOffset = 100.0
        tab2.homepageScrollOffset = 300.0
        XCTAssertEqual(tab1.homepageScrollOffset, 100.0)
        XCTAssertEqual(tab2.homepageScrollOffset, 300.0)
    }

    // Behavioral: scrollViewDidEndDragging saves the current scroll position to the active tab
    func testScrollViewDidEndDraggingSavesOffsetToActiveTab() {
        let tabManager = HomepageScrollTabManager()
        let tab = MockTab(profile: MockProfile(), windowUUID: .XCTestDefaultUUID)
        tabManager.registerTab(tab)

        let vc = HomepageViewController(
            windowUUID: .XCTestDefaultUUID,
            tabManager: tabManager,
            overlayManager: MockOverlayModeManager(),
            toastContainer: UIView()
        )
        vc.loadViewIfNeeded()

        let scrollView = UIScrollView()
        scrollView.contentOffset = CGPoint(x: 0, y: 250.0)
        vc.scrollViewDidEndDragging(scrollView, willDecelerate: false)

        XCTAssertEqual(tab.homepageScrollOffset, 250.0,
                       "scrollViewDidEndDragging must save the current contentOffset.y to the active tab")
    }

    // Behavioral: restoreVerticalScrollOffset sets the collection view offset to the saved value
    func testRestoreVerticalScrollOffsetSetsCollectionViewOffset() {
        let tabManager = HomepageScrollTabManager()
        let tab = MockTab(profile: MockProfile(), windowUUID: .XCTestDefaultUUID)
        tab.homepageScrollOffset = 200.0
        tabManager.registerTab(tab)

        let vc = HomepageViewController(
            windowUUID: .XCTestDefaultUUID,
            tabManager: tabManager,
            overlayManager: MockOverlayModeManager(),
            toastContainer: UIView()
        )
        vc.loadViewIfNeeded()
        vc.restoreVerticalScrollOffset()

        let collectionView = vc.view.subviews.first(where: { $0 is UICollectionView }) as? UICollectionView
        XCTAssertEqual(collectionView?.contentOffset.y, 200.0,
                       "restoreVerticalScrollOffset must set the collection view offset to the saved value")
    }
}
