import XCTest
import CoreLocation
@testable import OpenGpxTracker

final class AnvilTask9F2PTests: XCTestCase {

    // MARK: - CLActivityType extension

    func testActivityTypeNameExists() {
        let name = CLActivityType.other.name
        XCTAssertEqual(name, "Automatic",
                       ".other activity type should be named 'Automatic'")
    }

    func testActivityTypeDescriptionExists() {
        let desc = CLActivityType.other.description
        XCTAssertEqual(desc, "System default. Automatically selects the mode")
    }

    func testActivityTypeCountIs5() {
        XCTAssertEqual(CLActivityType.count, 5,
                       "There should be 5 activity types")
    }

    func testAutomotiveNavigationName() {
        XCTAssertEqual(CLActivityType.automotiveNavigation.name, "Automotive navigation")
    }

    func testFitnessName() {
        XCTAssertEqual(CLActivityType.fitness.name, "Fitness")
    }

    // MARK: - Preferences section constant

    func testActivityTypeSectionExists() {
        XCTAssertEqual(kActivityTypeSection, 3,
                       "Activity type section should be at index 3")
    }

    func testActivityTypeDefaultsKeyExists() {
        XCTAssertEqual(kDefaultsKeyActivityType, "ActivityType",
                       "UserDefaults key should be 'ActivityType'")
    }

    func testSectionCountIncreasedTo4() {
        let vc = PreferencesTableViewController(style: .grouped)
        let sections = vc.numberOfSections(in: vc.tableView)
        XCTAssertEqual(sections, 4,
                       "Preferences should have 4 sections after adding activity type")
    }

    // MARK: - Preferences: locationActivityType

    func testLocationActivityTypeDefaultsToOther() {
        let prefs = Preferences.shared
        XCTAssertEqual(prefs.locationActivityType, .other,
                       "Default activity type should be .other (Automatic)")
    }
}
