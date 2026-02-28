## Fix: Localization cleanup and encoding normalization

### Problem Description

The **ACHNBrowserUI** project supports multiple languages, but the localization files have accumulated several issues that cause incorrect string display, ambiguous lookups, and broken locale loading:

- Multiple `.strings` files contain **duplicate translation keys** within the same language (e.g., the same key appearing in two different comment sections). The last occurrence wins at runtime, making the effective translation unpredictable and inconsistent with translator intent.
- Some files have **encoding inconsistencies** — invisible control characters differ between languages for the same key (e.g., "X-Large"), and the Italian file has syntax errors (missing quotes and semicolons) that prevent correct parsing.
- The **Traditional Chinese locale** uses a non-standard identifier (`ZH_TW` / `zh_tw`), which iOS does not recognize as a valid locale. Translations for Traditional Chinese never load.
- The **Japanese `InfoPlist.strings`** contains text copied from the German localization, resulting in German privacy descriptions appearing for Japanese users.
- Translation keys in one language don't match the keys used in the app code (e.g., casing differences), causing fallback to the base language.

### Expected Behavior

- Each translation key appears exactly once per language file — no duplicates.
- All `.strings` files use consistent encoding with no stray control characters.
- Syntax errors in `.strings` files are corrected so all translations parse and load.
- The Traditional Chinese locale uses a valid Apple locale identifier and its translations load correctly at runtime.
- Misattributed locale resources are removed or corrected.
- Translation keys match the casing used in the application code.
- The project builds and all localized strings render correctly for supported languages.

### Acceptance Criteria

1. Duplicate translation keys are removed across all supported languages.
2. Encoding and syntax errors in `.strings` files are fixed.
3. The Traditional Chinese locale uses a correct identifier recognized by iOS.
4. Misattributed locale resources are removed or corrected.
5. The application builds successfully and localized strings display correctly.
