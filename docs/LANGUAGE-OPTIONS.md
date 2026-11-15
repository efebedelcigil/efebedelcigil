# English and Turkish profile options

## Recommendation

Keep English as the default profile and offer a small **English · Türkçe** link row leading to a generated `README.tr.md`. This is feasible without page JavaScript and would work on desktop and mobile. It has been evaluated here; the Turkish page and language controls have not been added.

GitHub displays the profile's default README rather than providing a native per-visitor language toggle. A translated Markdown page is a separate navigation destination, not an in-place website switch. GitHub supports relative links between repository documents; see [the official Markdown guidance](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

Most visible text in this profile is SVG path artwork. Adding a Turkish link alone would leave those images in English, and browser text translation cannot translate glyph outlines. A complete bilingual version needs localized artwork as well as a translated Markdown wrapper.

## Implementation outline

1. Store translated interface copy in a small locale dictionary. Keep brand/tool names, repository names and language identifiers unchanged.
2. Generate English and Turkish section titles, status/area copy, portfolio/footer labels and accessible image descriptions from the same layout functions.
3. Reuse robot raster frames, component PNGs, contribution dates/counts, pinned repository selection and language distributions. Do not maintain a second live-data fetch.
4. Generate `README.md`, `README.tr.md` and both still pages with correct relative asset links and matching geometry. Keep `main` publication atomic so all locales use the same snapshot.
5. Add two discreet ordinary text links near the top. Avoid flags, a dropdown, automatic browser-language redirects or doubled full-page content.
6. Extend the current label/icon and theme/still tests to both locales, especially longer Turkish text and characters.

| Alternative | Assessment |
| --- | --- |
| Separate generated Turkish README | Recommended: complete translation, shared data, explicit navigation |
| Two full languages in the main README | Doubles page density; conflicts with the accepted quieter layout |
| Turkish text inside a disclosure | Compact, but leaves SVG artwork untranslated and provides a different experience |
| Automatic/in-place language selector | Requires website-level scripting/hosting that this README does not provide |

The portfolio can keep its own language navigation independently. No portfolio repository was modified during this profile work.
