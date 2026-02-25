## Feature: Add initial speech recognition engine for voice search

### Problem Description

**Firefox iOS** is adding voice search support. The first step is to integrate Apple's speech recognition framework to provide on-device speech-to-text transcription. The existing voice search package defines a service protocol and a result type, but has no real transcription engine — only a mock implementation for testing.

A production-quality transcription engine is needed that:
- Manages microphone and speech-recognition permissions.
- Configures the audio session for recording.
- Captures microphone audio and streams it to the speech recognizer.
- Yields partial and final transcription results via an async stream.
- Supports on-device recognition for privacy.

### Acceptance Criteria

1. A new transcription engine encapsulates the full speech recognition pipeline with thread-safe isolation.
2. A protocol defines the interface for swappable transcription engines (prepare, start, stop).
3. The existing speech error type gains cases for when the recognizer is unavailable and when permissions are denied.
4. A permissions handler checks both microphone and speech-recognition authorization.
5. Apple frameworks (audio engine, audio session, speech recognizer, authorization) are abstracted behind protocols for testability.
6. Preparing the engine throws when either microphone or speech permission is denied.
7. Preparing the engine configures the audio session for recording with measurement mode when permissions are granted.
