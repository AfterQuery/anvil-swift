import XCTest
import UIKit
@testable import Client

@MainActor
final class AnvilTask1F2PTests: XCTestCase, FeatureFlaggable {

    override func setUp() async throws {
        try await super.setUp()
        DependencyHelperMock().bootstrapDependencies()
        LegacyFeatureFlagsManager.shared.initializeDeveloperFeatures(with: MockProfile())
    }

    override func tearDown() async throws {
        DependencyHelperMock().reset()
        try await super.tearDown()
    }

    func testIsHomepageStoriesScrollDirectionCustomizedPropertyExists() {
        XCTAssertFalse(isHomepageStoriesScrollDirectionCustomized,
                       "Default scroll direction should not be customized")
    }

    func testIsHomepageStoriesScrollDirectionCustomizedReturnsBool() {
        // Compile-time check: the property returns Bool (not Any or Optional).
        let _: Bool = isHomepageStoriesScrollDirectionCustomized
    }

    func testScrollDirectionBaselineExists() {
        // ScrollDirection.baseline is the new default case added by the patch.
        // This will fail to compile on the base commit.
        let _: ScrollDirection = .baseline
    }

    func testScrollDirectionBaselineIsNotCustomized() {
        // When no custom experiment state overrides the default (.baseline), the
        // property must return false regardless of device type.
        // scrollDirection == .baseline  →  scrollDirection != .baseline  == false
        XCTAssertFalse(isHomepageStoriesScrollDirectionCustomized)
    }

    func testHomepageViewControllerScrollToTopDoesNotCrash() {
        // The patch changes scrollToTop to account for adjustedContentInset.
        // Both the zero-argument and the animated: overload must remain callable.
        let vc = HomepageViewController(
            windowUUID: .XCTestDefaultUUID,
            tabManager: MockTabManager(),
            overlayManager: MockOverlayModeManager(),
            toastContainer: UIView()
        )
        vc.loadViewIfNeeded()
        vc.scrollToTop()
        vc.scrollToTop(animated: false)
    }

    func testStoriesFeedCellTypeExists() {
        // StoriesFeedCell is a new UICollectionViewCell subclass registered for
        // the vertical stories experiment. This will fail to compile on the base commit.
        let cell = StoriesFeedCell(frame: .zero)
        XCTAssertNotNil(cell)
    }
}
