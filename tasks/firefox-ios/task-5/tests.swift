import XCTest
@testable import Client

@MainActor
final class AnvilTask5F2PTests: XCTestCase {

    override func setUp() async throws {
        try await super.setUp()
        DependencyHelperMock().bootstrapDependencies()
    }

    override func tearDown() async throws {
        DependencyHelperMock().reset()
        try await super.tearDown()
    }

    func testDispatchAvailableContentHeightChangedActionIsAccessible() {
        let bvc = BrowserViewController(
            profile: MockProfile(),
            tabManager: MockTabManager(),
            windowUUID: .XCTestDefaultUUID
        )
        bvc.dispatchAvailableContentHeightChangedAction()
    }
}
