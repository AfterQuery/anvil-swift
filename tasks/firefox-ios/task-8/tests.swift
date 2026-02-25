import XCTest
@testable import Client

@MainActor
final class AnvilTask8F2PTests: XCTestCase {

    override func setUp() async throws {
        try await super.setUp()
        DependencyHelperMock().bootstrapDependencies()
        LegacyFeatureFlagsManager.shared.initializeDeveloperFeatures(with: MockProfile())
    }

    override func tearDown() async throws {
        DependencyHelperMock().reset()
        try await super.tearDown()
    }

    func testTabHasHomepageScrollOffsetProperty() {
        let tab = MockTab(profile: MockProfile(), windowUUID: .XCTestDefaultUUID)
        XCTAssertNil(tab.homepageScrollOffset)
        tab.homepageScrollOffset = 200.0
        XCTAssertEqual(tab.homepageScrollOffset, 200.0)
    }

    func testHomepageViewControllerInitWithTabManager() {
        let vc = HomepageViewController(
            windowUUID: .XCTestDefaultUUID,
            tabManager: MockTabManager(),
            overlayManager: MockOverlayModeManager(),
            toastContainer: UIView()
        )
        XCTAssertNotNil(vc)
    }

    func testHomepageViewControllerHasRestoreVerticalScrollOffset() {
        let vc = HomepageViewController(
            windowUUID: .XCTestDefaultUUID,
            tabManager: MockTabManager(),
            overlayManager: MockOverlayModeManager(),
            toastContainer: UIView()
        )
        vc.loadViewIfNeeded()
        vc.restoreVerticalScrollOffset()
    }
}
