import XCTest
import CoreLocation
@testable import OpenGpxTracker

final class AnvilTask9F2PTests: XCTestCase {

    // MARK: - CLActivityType extension

    func testActivityTypeNameExists() {
        let name = CLActivityType.other.name
        XCTAssertFalse(name.isEmpty,
                       ".other activity type should have a non-empty display name")
    }

    func testActivityTypeDescriptionExists() {
        let desc = CLActivityType.other.description
        XCTAssertFalse(desc.isEmpty,
                       ".other activity type should have a non-empty description")
    }

    func testActivityTypeCountIs5() {
        XCTAssertEqual(CLActivityType.count, 5,
                       "There should be 5 activity types")
    }

    func testAutomotiveNavigationName() {
        XCTAssertFalse(CLActivityType.automotiveNavigation.name.isEmpty,
                       "Automotive navigation should have a non-empty name")
    }

    func testFitnessName() {
        XCTAssertFalse(CLActivityType.fitness.name.isEmpty,
                       "Fitness should have a non-empty name")
    }

    // MARK: - Preferences section constant

    func testActivityTypeSectionExists() {
        XCTAssertGreaterThanOrEqual(kActivityTypeSection, 0,
                                    "Activity type section should be a valid section index")
    }

    func testActivityTypeDefaultsKeyExists() {
        XCTAssertFalse(kDefaultsKeyActivityType.isEmpty,
                       "UserDefaults key should be a non-empty string")
    }

    func testSectionCountIncludesActivityType() {
        let vc = PreferencesTableViewController(style: .grouped)
        let sections = vc.numberOfSections(in: vc.tableView)
        XCTAssertGreaterThanOrEqual(sections, 4,
                                    "Preferences should have at least 4 sections after adding activity type")
    }

    // MARK: - Preferences: locationActivityType

    func testLocationActivityTypeDefaultsToOther() {
        let prefs = Preferences.shared
        XCTAssertEqual(prefs.locationActivityType, .other,
                       "Default activity type should be .other (Automatic)")
    }
}
