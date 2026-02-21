import XCTest
@testable import Backend

final class AnvilTask1Tests: XCTestCase {

    // Fish active all 12 months, ALL DAY (activeTimes: ["0","0"])
    private let allDayFishJSON = """
    {"total":1,"results":[{
        "id":90001,"name":"AllDayTestFish","category":"Fish",
        "content":{
            "name":"AllDayTestFish","sell":100,
            "category":"Fish","critterId":901,"internalID":9001,
            "activeMonths":{
                "0":{"activeTimes":["0","0"]},"1":{"activeTimes":["0","0"]},
                "2":{"activeTimes":["0","0"]},"3":{"activeTimes":["0","0"]},
                "4":{"activeTimes":["0","0"]},"5":{"activeTimes":["0","0"]},
                "6":{"activeTimes":["0","0"]},"7":{"activeTimes":["0","0"]},
                "8":{"activeTimes":["0","0"]},"9":{"activeTimes":["0","0"]},
                "10":{"activeTimes":["0","0"]},"11":{"activeTimes":["0","0"]}
            },
            "uniqueEntryID":"anvil_test_allday"
        },
        "variations":[]
    }]}
    """

    // Fish active all 12 months, 4 AM – 9 PM
    private let timedFishJSON = """
    {"total":1,"results":[{
        "id":90002,"name":"TimedTestFish","category":"Fish",
        "content":{
            "name":"TimedTestFish","sell":100,
            "category":"Fish","critterId":902,"internalID":9002,
            "activeMonths":{
                "0":{"activeTimes":["4am","9pm"]},"1":{"activeTimes":["4am","9pm"]},
                "2":{"activeTimes":["4am","9pm"]},"3":{"activeTimes":["4am","9pm"]},
                "4":{"activeTimes":["4am","9pm"]},"5":{"activeTimes":["4am","9pm"]},
                "6":{"activeTimes":["4am","9pm"]},"7":{"activeTimes":["4am","9pm"]},
                "8":{"activeTimes":["4am","9pm"]},"9":{"activeTimes":["4am","9pm"]},
                "10":{"activeTimes":["4am","9pm"]},"11":{"activeTimes":["4am","9pm"]}
            },
            "uniqueEntryID":"anvil_test_timed"
        },
        "variations":[]
    }]}
    """

    private func decodeFirst(_ json: String) -> Item {
        let response = try! JSONDecoder().decode(
            NewItemResponse.self,
            from: json.data(using: .utf8)!
        )
        return response.results.first!.content
    }

    // MARK: - isActiveThisMonth (renamed from isActive)

    func testIsActiveThisMonthForAllYearFish() {
        let fish = decodeFirst(allDayFishJSON)
        XCTAssertTrue(fish.isActiveThisMonth(),
                       "Fish active every month should be active this month")
    }

    // MARK: - isActiveAtThisHour

    func testIsActiveAtThisHourAllDayFish() {
        let fish = decodeFirst(allDayFishJSON)
        XCTAssertTrue(fish.isActiveAtThisHour(),
                       "All-day fish should always be active at the current hour")
    }

    func testIsActiveAtThisHourReturnsBool() {
        let fish = decodeFirst(timedFishJSON)
        let _: Bool = fish.isActiveAtThisHour()
    }

    // MARK: - filterActiveThisMonth (renamed from filterActive)

    func testFilterActiveThisMonth() {
        let fish = decodeFirst(allDayFishJSON)
        let active = [fish].filterActiveThisMonth()
        XCTAssertEqual(active.count, 1,
                        "All-year fish should appear in filterActiveThisMonth results")
    }

    // MARK: - formattedTimes still works

    func testFormattedTimesForTimedFish() {
        let fish = decodeFirst(timedFishJSON)
        let times = fish.formattedTimes()
        XCTAssertNotNil(times, "Timed fish should return a non-nil formatted time string")
    }

    func testFormattedTimesAllDayFish() {
        let fish = decodeFirst(allDayFishJSON)
        let times = fish.formattedTimes()
        XCTAssertNotNil(times, "All-day fish should return a formatted time string")
    }
}
