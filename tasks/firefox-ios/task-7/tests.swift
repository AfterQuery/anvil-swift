import XCTest
@testable import VoiceSearchKit

final class AnvilTask7F2PTests: XCTestCase {

    func testSpeechErrorRecognizerNotAvailableCaseExists() {
        let error = SpeechError.recognizerNotAvailable
        XCTAssertEqual(error, SpeechError.recognizerNotAvailable)
    }

    func testSpeechErrorPermissionDeniedCaseExists() {
        let error = SpeechError.permissionDenied
        XCTAssertEqual(error, SpeechError.permissionDenied)
    }

    func testSpeechErrorConformsToEquatable() {
        XCTAssertNotEqual(SpeechError.recognizerNotAvailable, SpeechError.permissionDenied)
        XCTAssertNotEqual(SpeechError.recognizerNotAvailable, SpeechError.unknown)
        XCTAssertNotEqual(SpeechError.permissionDenied, SpeechError.unknown)
    }

    func testSpeechErrorConformsToError() {
        let error: Error = SpeechError.recognizerNotAvailable
        XCTAssertNotNil(error)
    }
}
