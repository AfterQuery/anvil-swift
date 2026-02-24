import XCTest
@testable import Client

@MainActor
final class AnvilTask2F2PTests: XCTestCase {

    private var profile: MockProfile!
    private var tabManager: MockTabManager!

    override func setUp() async throws {
        try await super.setUp()
        DependencyHelperMock().bootstrapDependencies()
        profile = MockProfile()
        tabManager = MockTabManager()
    }

    override func tearDown() async throws {
        profile = nil
        tabManager = nil
        DependencyHelperMock().reset()
        try await super.tearDown()
    }

    func testRelayMaskSettingsViewControllerInitWithTabManager() {
        let vc = RelayMaskSettingsViewController(
            profile: profile,
            windowUUID: .XCTestDefaultUUID,
            tabManager: tabManager
        )
        XCTAssertNotNil(vc)
    }

    func testManageRelayMaskSettingHasManageMasksURL() throws {
        let vc = RelayMaskSettingsViewController(
            profile: profile,
            windowUUID: .XCTestDefaultUUID,
            tabManager: tabManager
        )
        let settings = vc.generateSettings()
        let section = try XCTUnwrap(settings.last)
        let setting = try XCTUnwrap(section.children.first as? ManageRelayMasksSetting)
        XCTAssertNotNil(setting.manageMasksURL)
    }
}
