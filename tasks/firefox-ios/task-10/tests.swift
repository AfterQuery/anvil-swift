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

    // Behavioral: URL without badcert param must return nil
    func testCertificateDataFromErrorURLReturnsNilWithoutParam() {
        let url = URL(string: "internal://local/errorpage")!
        XCTAssertNil(CertificateHelper.certificateDataFromErrorURL(url),
                     "URL with no badcert query param must return nil certificate data")
    }

    // Behavioral: URL with a valid base64 cert produces non-nil data
    func testCertificateDataFromErrorURLReturnsDataForValidBase64Param() {
        let fakeDER = Data([0x30, 0x00])
        let encoded = fakeDER.base64EncodedString()
            .addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed)!
        let url = URL(string: "internal://local/errorpage?badcert=\(encoded)")!
        XCTAssertNotNil(CertificateHelper.certificateDataFromErrorURL(url),
                        "URL with valid base64 badcert param must return non-nil Data")
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
