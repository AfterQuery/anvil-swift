import XCTest
@testable import Client

@MainActor
final class AnvilTask10F2PTests: XCTestCase {

    override func setUp() async throws {
        try await super.setUp()
        DependencyHelperMock().bootstrapDependencies()
    }

    override func tearDown() async throws {
        DependencyHelperMock().reset()
        try await super.tearDown()
    }

    func testCertificateHelperExists() {
        let url = URL(string: "internal://local/errorpage?badcert=test")!
        _ = CertificateHelper.certificateDataFromErrorURL(url)
    }

    func testCertificateHelperCertificatesFromErrorURL() {
        let url = URL(string: "internal://local/errorpage?badcert=test")!
        _ = CertificateHelper.certificatesFromErrorURL(url, logger: DefaultLogger.shared)
    }

    func testNativeErrorPageViewControllerAcceptsTabManager() {
        let overlayManager = MockOverlayModeManager()
        let tabManager = MockTabManager()
        let _ = NativeErrorPageViewController(
            windowUUID: .XCTestDefaultUUID,
            overlayManager: overlayManager,
            tabManager: tabManager
        )
    }
}
