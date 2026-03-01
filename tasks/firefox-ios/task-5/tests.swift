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
        // CertificateHelper is a new type added by the patch.
        // This will fail to compile on the base commit.
        let url = URL(string: "internal://local/errorpage?cert=test")!
        _ = CertificateHelper.certificate(from: url)
    }

    func testNativeErrorPageViewControllerHasViewCertificateHandler() {
        // didTapViewCertificate() is added by the patch.
        // This will fail to compile on the base commit.
        let vc = NativeErrorPageViewController(
            url: URL(string: "internal://local/errorpage")!,
            windowUUID: .XCTestDefaultUUID
        )
        vc.didTapViewCertificate()
    }

    func testNativeErrorPageViewControllerHasLearnMoreHandler() {
        // didTapLearnMore() is added by the patch.
        // This will fail to compile on the base commit.
        let vc = NativeErrorPageViewController(
            url: URL(string: "internal://local/errorpage")!,
            windowUUID: .XCTestDefaultUUID
        )
        vc.didTapLearnMore()
    }
}
