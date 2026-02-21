import XCTest
@testable import Backend

final class AnvilTask3Tests: XCTestCase {

    // MARK: - Helpers

    private func makeItem(
        name: String = "TestItem",
        filename: String = "anvil_test_item",
        variationCount: Int
    ) -> Item {
        let variants: String
        if variationCount > 0 {
            let entries = (0..<variationCount).map { i in
                "{\"id\":\(60000+i),\"content\":{\"image\":\"img\(i)\",\"colors\":[\"C\(i)\"]}}"
            }
            variants = entries.joined(separator: ",")
        } else {
            variants = ""
        }

        let json = """
        {
            "name":"\(name)",
            "category":"Housewares",
            "filename":"\(filename)",
            "variations":[\(variants)]
        }
        """
        return try! JSONDecoder().decode(Item.self, from: json.data(using: .utf8)!)
    }

    // MARK: - hasSomeVariations

    func testHasSomeVariationsWithMultiple() {
        let item = makeItem(variationCount: 3)
        XCTAssertTrue(item.hasSomeVariations,
                       "Item with 3 variants should report hasSomeVariations == true")
    }

    func testHasSomeVariationsWithOne() {
        let item = makeItem(variationCount: 1)
        XCTAssertFalse(item.hasSomeVariations,
                        "Item with 1 variant should not count as having variations")
    }

    func testHasSomeVariationsWithNone() {
        let item = makeItem(variationCount: 0)
        XCTAssertFalse(item.hasSomeVariations,
                        "Item with 0 variants should not count as having variations")
    }

    // MARK: - VariantsCompletionStatus enum

    func testVariantsCompletionStatusEnumCases() {
        let _: VariantsCompletionStatus = .unstarted
        let _: VariantsCompletionStatus = .partial
        let _: VariantsCompletionStatus = .complete
    }

    // MARK: - completionStatus(for:)

    func testCompletionStatusUnstartedWhenEmpty() {
        let item = makeItem(variationCount: 3)
        let dict: [String: [Variant]] = [:]
        XCTAssertEqual(dict.completionStatus(for: item), .unstarted)
    }

    func testCompletionStatusPartial() {
        let item = makeItem(variationCount: 3)
        let oneVariant = item.variations![0]
        let dict: [String: [Variant]] = ["anvil_test_item": [oneVariant]]
        XCTAssertEqual(dict.completionStatus(for: item), .partial)
    }

    func testCompletionStatusComplete() {
        let item = makeItem(variationCount: 3)
        let dict: [String: [Variant]] = ["anvil_test_item": item.variations!]
        XCTAssertEqual(dict.completionStatus(for: item), .complete)
    }

    // MARK: - toggleVariant auto-manages parent item

    func testToggleVariantAutoAddsParentItem() {
        let collection = UserCollection(iCloudDisabled: true)
        let item = makeItem(variationCount: 3)
        let variant = item.variations![0]

        XCTAssertFalse(collection.items.contains(item),
                        "Item should not be in collection before any toggle")

        _ = collection.toggleVariant(item: item, variant: variant)

        XCTAssertTrue(collection.items.contains(item),
                       "Toggling first variant should auto-add the parent item to the collection")
    }

    func testToggleLastVariantAutoRemovesParentItem() {
        let collection = UserCollection(iCloudDisabled: true)
        let item = makeItem(variationCount: 3)
        let variant = item.variations![0]

        _ = collection.toggleVariant(item: item, variant: variant)
        XCTAssertTrue(collection.items.contains(item))

        _ = collection.toggleVariant(item: item, variant: variant)
        XCTAssertFalse(collection.items.contains(item),
                        "Removing the last liked variant should auto-remove the parent item")
    }
}
