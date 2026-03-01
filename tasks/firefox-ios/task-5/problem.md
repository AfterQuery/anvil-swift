## Feature: Certificate Modal Support for Native Error Pages

### Problem Description

In **Firefox iOS**, when a user encounters a TLS/certificate error (e.g., `NET::ERR_CERT_AUTHORITY_INVALID`), the native error page is shown via `NativeErrorPageViewController`. However, the error page currently lacks the ability to:

1. Display certificate details to the user via a modal sheet.
2. Parse certificate data embedded in the error URL so it can be presented.
3. Handle the "Learn More" action that opens an informational resource about the certificate error.

The certificate data is embedded in the error URL as query parameters and needs to be extracted and decoded before it can be shown to the user.

### Acceptance Criteria

1. A `CertificateHelper` type must exist that can parse certificate data from a native error page URL.
2. `NativeErrorPageViewController` must implement a `didTapViewCertificate()` handler that presents the certificate detail modal using the parsed certificate data.
3. `NativeErrorPageViewController` must implement a `didTapLearnMore()` handler that opens the appropriate support URL.
4. `ErrorPageHelper` must expose a method/extension for extracting certificate data from an error URL.
5. All new code paths must have corresponding unit tests.
