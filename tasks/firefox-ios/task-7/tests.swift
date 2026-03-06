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

    // Behavioral: each case must be a distinct, non-empty error (all three cases must exist and differ)
    func testAllThreeSpeechErrorCasesAreDistinct() {
        let allCases: [SpeechError] = [.recognizerNotAvailable, .permissionDenied, .unknown]
        // Verify all three cases produce distinct values
        XCTAssertEqual(Set(allCases).count, 3,
                       "All three SpeechError cases must be distinct")
    }

    // Behavioral: prepare() must throw .permissionDenied when mic permission is denied.
    // Uses mock providers that deny permission to exercise the permission-check path.
    func testPrepareThrowsPermissionDeniedWhenMicrophoneAccessDenied() async {
        let mockSession = MockAudioSession(micPermissionGranted: false)
        let authorizer = AuthorizationHandler(audioSession: mockSession)
        let engine = SpeechRecognitionEngine(
            audioEngine: MockAudioEngine(),
            audioSession: mockSession,
            speechRecognizer: MockSpeechRecognizer(isAvailable: true),
            authorizer: authorizer
        )
        do {
            try await engine.prepare()
            XCTFail("prepare() must throw when microphone permission is denied")
        } catch let error as SpeechError {
            XCTAssertEqual(error, .permissionDenied,
                           "prepare() must throw .permissionDenied when mic access is denied")
        }
    }
}
