import XCTest
import UIKit
@testable import OpenGpxTracker

final class AnvilTask1F2PTests: XCTestCase {

    // MARK: - GPXTileServerColorMode enum

    func testColorModeEnumCases() {
        let _: GPXTileServer.GPXTileServerColorMode = .lightMode
        let _: GPXTileServer.GPXTileServerColorMode = .system
        let _: GPXTileServer.GPXTileServerColorMode = .darkMode
    }

    func testAppleSatelliteIsDarkMode() {
        XCTAssertEqual(GPXTileServer.appleSatellite.colorMode,
                       GPXTileServer.GPXTileServerColorMode.darkMode,
                       "Apple Satellite should use dark mode color scheme")
    }

    func testAppleIsSystemMode() {
        XCTAssertEqual(GPXTileServer.apple.colorMode,
                       GPXTileServer.GPXTileServerColorMode.system,
                       "Default Apple map should follow system appearance")
    }

    func testOpenStreetMapIsLightMode() {
        XCTAssertEqual(GPXTileServer.openStreetMap.colorMode,
                       GPXTileServer.GPXTileServerColorMode.lightMode,
                       "OpenStreetMap should use light mode color scheme")
    }

    func testCartoDBIsLightMode() {
        XCTAssertEqual(GPXTileServer.cartoDB.colorMode,
                       GPXTileServer.GPXTileServerColorMode.lightMode,
                       "CartoDB should use light mode color scheme")
    }

    // MARK: - GPXScaleBar.forcedColor

    func testForcedColorDefaultsToNil() {
        let scaleBar = GPXScaleBar()
        XCTAssertNil(scaleBar.forcedColor,
                     "forcedColor should default to nil (system-adaptive)")
    }

    func testForcedColorCanBeSet() {
        let scaleBar = GPXScaleBar()
        scaleBar.forcedColor = .white
        XCTAssertEqual(scaleBar.forcedColor, .white)
        scaleBar.forcedColor = nil
        XCTAssertNil(scaleBar.forcedColor)
    }
}
