import XCTest
@testable import Client

@MainActor
final class AnvilTask6F2PTests: XCTestCase {

    override func setUp() async throws {
        try await super.setUp()
        DependencyHelperMock().bootstrapDependencies()
    }

    override func tearDown() async throws {
        DependencyHelperMock().reset()
        try await super.tearDown()
    }

    func testGetSkeletonAddressBarConfigurationForNilTab() {
        let model = AddressToolbarContainerModel(
            state: ToolbarState(windowUUID: .XCTestDefaultUUID),
            shouldAnimate: false,
            isTranslucent: false
        )
        let config = model.getSkeletonAddressBarConfiguration(for: nil)
        XCTAssertTrue(config.leadingPageActions.isEmpty)
        XCTAssertTrue(config.trailingPageActions.isEmpty)
        XCTAssertNil(config.locationViewConfiguration.url)
    }

    func testGetSkeletonAddressBarConfigurationForTabWithURL() {
        let model = AddressToolbarContainerModel(
            state: ToolbarState(windowUUID: .XCTestDefaultUUID),
            shouldAnimate: false,
            isTranslucent: false
        )
        let tab = MockTab(profile: MockProfile(), windowUUID: .XCTestDefaultUUID)
        tab.url = URL(string: "https://example.com")
        let config = model.getSkeletonAddressBarConfiguration(for: tab)

        XCTAssertEqual(config.leadingPageActions.count, 1)
        XCTAssertEqual(config.trailingPageActions.count, 1)
        XCTAssertEqual(config.locationViewConfiguration.url, tab.url)
    }

    func testGetSkeletonAddressBarConfigurationEmptyNavAndBrowserActions() {
        let model = AddressToolbarContainerModel(
            state: ToolbarState(windowUUID: .XCTestDefaultUUID),
            shouldAnimate: false,
            isTranslucent: false
        )
        let tab = MockTab(profile: MockProfile(), windowUUID: .XCTestDefaultUUID)
        tab.url = URL(string: "https://example.com")
        let config = model.getSkeletonAddressBarConfiguration(for: tab)

        XCTAssertTrue(config.navigationActions.isEmpty)
        XCTAssertTrue(config.browserActions.isEmpty)
    }
}
