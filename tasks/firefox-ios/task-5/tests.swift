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

    func testCertificateHelperExists() {
        let url = URL(string: "internal://local/errorpage?badcert=test")!
        _ = CertificateHelper.certificateDataFromErrorURL(url)
    }

    // Behavioral: URL without cert param must return nil — no spurious cert data
    func testCertificateHelperReturnsNilForURLWithoutCertParam() {
        let url = URL(string: "internal://local/errorpage")!
        XCTAssertNil(CertificateHelper.certificateDataFromErrorURL(url),
                     "URL with no certificate query param must return nil")
    }

    // Behavioral: URL with a valid base64 cert param must produce non-nil certificate data
    func testCertificateHelperReturnsNonNilForURLWithValidBase64CertParam() {
        // Minimal valid DER encoding: SEQUENCE { } — 3 bytes, valid ASN.1 for testing the parse path
        let fakeDER = Data([0x30, 0x00])
        let encoded = fakeDER.base64EncodedString()
            .addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed)!
        let url = URL(string: "internal://local/errorpage?badcert=\(encoded)")!
        // The certificate may not be trusted, but the data-parsing path must not return nil
        XCTAssertNotNil(CertificateHelper.certificateDataFromErrorURL(url),
                        "URL with a valid base64 badcert param must return non-nil certificate data")
    }

    func testNativeErrorPageViewControllerHasViewCertificateHandler() {
        let vc = NativeErrorPageViewController(
            windowUUID: .XCTestDefaultUUID,
            overlayManager: MockOverlayModeManager(),
            tabManager: MockTabManager()
        )
        XCTAssertTrue(vc.responds(to: Selector("didTapViewCertificate")),
                      "NativeErrorPageViewController must implement didTapViewCertificate()")
    }

    func testNativeErrorPageViewControllerHasLearnMoreHandler() {
        let vc = NativeErrorPageViewController(
            windowUUID: .XCTestDefaultUUID,
            overlayManager: MockOverlayModeManager(),
            tabManager: MockTabManager()
        )
        XCTAssertTrue(vc.responds(to: Selector("didTapLearnMore")),
                      "NativeErrorPageViewController must implement didTapLearnMore()")
    }
}
