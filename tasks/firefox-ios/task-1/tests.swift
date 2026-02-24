import XCTest
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
}
