import XCTest
@testable import Client

@MainActor
final class AnvilTask9F2PTests: XCTestCase {

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

    // Behavioral: tapping "Manage email masks" must open a new browser tab
    func testManageRelayMaskSettingOpensNewTab() throws {
        let vc = RelayMaskSettingsViewController(
            profile: profile,
            windowUUID: .XCTestDefaultUUID,
            tabManager: tabManager
        )
        let settings = vc.generateSettings()
        let section = try XCTUnwrap(settings.last)
        let setting = try XCTUnwrap(section.children.first as? ManageRelayMasksSetting)

        let tabCountBefore = tabManager.addTabsForURLsCalled
        setting.onClick(nil)
        XCTAssertGreaterThan(tabManager.addTabsForURLsCalled, tabCountBefore,
                             "Tapping manage masks must open a new tab via TabManager")
    }

    // Behavioral: the URL opened must match the setting's declared manageMasksURL
    func testManageRelayMaskSettingOpensCorrectURL() throws {
        let vc = RelayMaskSettingsViewController(
            profile: profile,
            windowUUID: .XCTestDefaultUUID,
            tabManager: tabManager
        )
        let settings = vc.generateSettings()
        let section = try XCTUnwrap(settings.last)
        let setting = try XCTUnwrap(section.children.first as? ManageRelayMasksSetting)
        let expectedURL = try XCTUnwrap(setting.manageMasksURL)

        setting.onClick(nil)
        XCTAssertTrue(tabManager.addTabsURLs.contains(expectedURL),
                      "The URL opened must match the setting's manageMasksURL")
    }
}
