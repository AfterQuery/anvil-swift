## Feature: Add custom chores and to-dos to the dashboard

### Problem Description

The dashboard currently tracks only predefined Daily Tasks. Users cannot add their own reminders, such as sending gifts, crafting items, or selling to NPCs. The app needs a lightweight todo list to track arbitrary player-defined chores. 

The feature should allow users to create, view, complete, delete, and reset chores while showing progress on the dashboard. Display logic and derived state must reside in view models to avoid direct view access to user data. The feature must integrate with existing task infrastructure without affecting Daily Tasks or other sections, and remain extensible for future enhancements like recurring chores or hiding completed items.

### Acceptance Criteria

1. Implement a `Chore` model with:
   - Initializers: `Chore()` and `Chore(title:description:isFinished:)`
   - Properties: `title: String`, `description: String`, `isFinished: Bool`, `id` used for identity-based equality

2. Implement a `UserCollection` type with:
   - Property: `chores: [Chore]`
   - Methods: `addChore(_:)`, `toggleChore(_:)`, `resetChores()`, `deleteChore(at:)`

3. Implement a `ChoreFormViewModel` with:
   - Initializer: `init(chore: Chore?)`
   - Property: `chore: Chore`

4. Implement a `ChoreListViewModel` with:
   - Property: `chores: [Chore]`
   - Computed properties: `shouldShowResetButton: Bool`, `shouldShowDescriptionView: Bool`

5. Implement a `TodayChoresSectionViewModel` with:
   - Property: `chores: [Chore]`
   - Computed properties: `totalChoresCount: Int`, `completeChoresCount: Int`

6. Ensure `TodaySection.SectionName.chores` is included in the default dashboard sections.

7. Users can:
   - Add chores from a dedicated list interface
   - Toggle completion
   - Delete chores
   - Reset completed chores

8. The dashboard chores section displays total and completed chore counts as a progress ratio.

9. View models handle all display logic and derived state; views do not directly access user data.

10. The implementation integrates with existing dashboard/task functionality without altering Daily Tasks or other sections, and allows for future enhancements such as recurring chores or hiding completed items.