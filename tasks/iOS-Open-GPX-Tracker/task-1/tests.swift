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

    func testForcedColorUpdatesScaleBarAppearance() {
        let scaleBar = GPXScaleBar()
        scaleBar.forcedColor = .white
        scaleBar.layoutIfNeeded()
        let barView = scaleBar.subviews.first
        XCTAssertTrue(barView?.backgroundColor?.isEqual(UIColor.white) == true,
                     "Setting forcedColor should update the scale bar's visual elements")
    }

    // MARK: - ViewController wiring (tile server drives label/scalebar color)

    func testViewControllerAppliesBlackToLabelsForLightModeTileServer() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let vc = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Could not load ViewController from storyboard")
            return
        }
        vc.loadViewIfNeeded()
        vc.map.tileServer = .openStreetMap
        vc.textColorAdaptations()
        XCTAssertTrue(vc.signalAccuracyLabel.textColor?.isEqual(UIColor.black) == true,
                      "Light-mode tile servers must use black overlay labels")
    }

    func testViewControllerAppliesWhiteToLabelsForDarkModeTileServer() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let vc = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Could not load ViewController from storyboard")
            return
        }
        vc.loadViewIfNeeded()
        vc.map.tileServer = .appleSatellite
        vc.textColorAdaptations()
        XCTAssertTrue(vc.signalAccuracyLabel.textColor?.isEqual(UIColor.white) == true,
                      "Dark-mode tile servers must use white overlay labels")
    }

    func testViewControllerAppliesForcedColorToScaleBarForTileServer() {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle(for: ViewController.self))
        guard let vc = storyboard.instantiateInitialViewController() as? ViewController else {
            XCTFail("Could not load ViewController from storyboard")
            return
        }
        vc.loadViewIfNeeded()
        guard let scaleBar = vc.map.scaleBar else {
            XCTFail("Map should have scale bar for color adaptation test")
            return
        }
        vc.map.tileServer = .openStreetMap
        vc.textColorAdaptations()
        XCTAssertTrue(scaleBar.forcedColor?.isEqual(UIColor.black) == true,
                     "Scale bar forcedColor must be driven by tile server selection")
    }
}
