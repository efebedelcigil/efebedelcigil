# Editing the profile

This guide describes the current generated README. Edit the sources below, not the generated SVGs or README: the next scheduled build replaces generated files.

## 1. Make a small edit

1. Open the appropriate source file in this repository and select **Edit**.
2. Change one item using the tables below. JSON requires double quotes and no trailing comma.
3. Commit the source change through the repository's normal review process.
4. Open **Actions → Public profile artwork**. Source changes listed in the workflow trigger a build; use **Run workflow** on `main` when needed.
5. Wait for the complete run, including **Publish generated profile without a pull request**. A successful branch run validates code but does not publish the profile.
6. Check the live profile in both themes and the **Still Version of Landing Page** link. GitHub's image proxy can delay visible changes.

Scheduled public data updates run every 15 minutes, subject to GitHub scheduling delays. They publish generated files directly to `main` using `PROFILE_PUBLISH_TOKEN`; they do not wait for an update PR. Never paste this secret into a file or a chat. The publisher skips stale output if `main` changes during generation.

## 2. Source map

| Visible content | Edit here | Exact change | Rebuild |
| --- | --- | --- | --- |
| Name | `scripts/build_hero.py` | Search for the name literal; retain text layout and timing | `refresh_hero.py` |
| Discipline | `assets/profile.json` → `discipline` | Replace the string | `refresh_hero.py` |
| University | `assets/profile.json` → `institution` | Replace the string | `refresh_hero.py` |
| Student/graduate status | `assets/profile.json` → `status` | For example, change `Final-Year Student` to `Graduate`; the discipline already identifies the degree | `refresh_hero.py` |
| GitHub and LinkedIn destinations | `scripts/build_readme.py` → social `linked()` calls | Change the URL, not the SVG | `build_readme.py`, `build_static.py` |
| Portfolio destination | `assets/profile.json` → `portfolio` | Full HTTPS URL | `build_readme.py`, `build_static.py` |
| Portfolio heading and description | `scripts/build_dashboard.py` → `title`, `subtitles` | Current copy: Explore My Portfolio / ALL projects, publications, contact info. and more | `build_dashboard.py` |
| Portfolio hand/click animation | `scripts/profile_visuals.py` → `click_cursor` | SVG hand path, eight-second timing and click cue | `build_dashboard.py` |
| Section headings | `scripts/build_dashboard.py` → section title loop | Change the visible title; keep internal keys such as `languages` and `pinned` stable | `build_dashboard.py` |
| Section order and accessible labels | `scripts/build_readme.py` → `parts` | Reorder complete sections; keep heading and content together | `build_readme.py` |
| Working Areas | `assets/profile.json` → `areas` | First two entries form the main line; later entries are supporting fields | `build_dashboard.py`, `build_readme.py` |
| In Progress area cards | `assets/profile.json` → `learning_area_groups` | Change a group's `tools` list; also update `learning_areas` for the accessible summary | `build_dashboard.py`, `build_readme.py` |
| Interested in Exploring area cards | `assets/profile.json` → `exploring_area_groups` | Change a group's `tools` list; also update `exploring_areas` | `build_dashboard.py`, `build_readme.py` |
| Tools cards | `assets/toolkit.json` | Category `name`, `color` and `tools`; colors are `blue`, `teal`, `warm` | `build_toolkit.py`, `build_readme.py` |
| In Progress tools/methods | `assets/learning.json` | Group `name` and `tools` | `build_dashboard.py`, `build_readme.py` |
| Interested in Exploring tools/methods | `assets/exploring.json` | Group `name` and `tools` | `build_dashboard.py`, `build_readme.py` |
| Small card left accents | `scripts/build_toolkit.py`, `scripts/design_parts.py` | `data-card-accent`; short static 2.5-unit-wide vertical mark, no moving miniature halo | Dashboard/toolkit builds |
| Brand logos | `assets/brand-map.json`, `assets/logos/` | Map the item label to an existing vendor SVG or add a licensed SVG | Dashboard/toolkit builds |
| Category/field icons | `assets/icon-map.json`, `assets/icons/` | Map the item label to an existing outline icon basename | Dashboard/toolkit builds |
| Contribution dates and levels | Automatic `assets/public-profile.json` | Do not edit; `public_calendar.py` reads the anonymous GitHub calendar | Scheduled workflow |
| Contribution PCB geometry | `scripts/contribution_geometry.py` | Projection, cell pitch, board fitting and centered origins | `build_dashboard.py` |
| Component sizing/current path | `scripts/contribution_routing.py` | Package clearance, type-consistent size, terminal selection, path and masking | `build_dashboard.py`, routing tests |
| Component models | `scripts/render_pcb_components.py` | Blender model geometry/materials; eight 0°/90° variants | Blender + preparation, then dashboard |
| Component image metadata | `scripts/prepare_pcb_components.py`, `scripts/refine_silhouettes.py` | Generated crop, contacts and opaque silhouette; do not hand-edit `layout.json` | Preparation after fresh renders |
| Less–More legend | `scripts/profile_visuals.py` → `legend_sprite`; dashboard legend loop | Five states, framed empty lands, proportional render samples | `build_dashboard.py` |
| Public Activity | Automatic snapshot; `scripts/build_dashboard.py` activity layout | Types include commits, issues, PRs, reviews and repository creation; total consistency is checked | Scheduled workflow |
| Most Used Languages | Automatic snapshot; dashboard language layout | Public non-fork source-code byte distribution, excluding this profile; not proficiency | Scheduled workflow |
| Featured Repositories selection/order | GitHub profile → Customize your pins | The cards still follow native public pins; the visible section title does not create a second selection list | Scheduled workflow |
| Featured card title/description | The public repository name/description on GitHub | Overflow is truncated by the generator | Scheduled workflow |
| Featured card languages | Automatic language API data | Do not type languages into SVG cards | Scheduled workflow |
| Footer links/sizes | `scripts/build_readme.py`, dashboard footer loop | Still version and Back to Top; widths follow text | Dashboard + README/static |
| Global palette/spacing | `scripts/build_dashboard.py`, `scripts/build_toolkit.py`, `scripts/design_parts.py` | Theme tokens, shared groups and section spacing; preserve matched light/dark geometry | Full build |
| Discovery links | `llms.txt` | Profile/portfolio/documentation URLs, no duplicated live metrics | No image rebuild |
| Crawling policy | `robots.txt`, `docs/DISCOVERY.md` | Applies only if deployed at a site's root; cannot control github.com | No image rebuild |

## 3. Every editable card

JSON paths below use zero-based array indexes. Names are source strings: display normalization may adjust capitalization. Edit `tools[index]` to rename an item, append a string to add one, or remove that string to delete it. If you reorder categories, their numeric paths change.

| Section | Category | Current card | Source and JSON path |
| --- | --- | --- | --- |
| Tools | Programming | C | `assets/toolkit.json` → `[0].tools[0]` |
| Tools | Programming | C++ | `assets/toolkit.json` → `[0].tools[1]` |
| Tools | Programming | Assembly | `assets/toolkit.json` → `[0].tools[2]` |
| Tools | Modeling & Simulation | MATLAB / Simulink | `assets/toolkit.json` → `[1].tools[0]` |
| Tools | Modeling & Simulation | PSIM | `assets/toolkit.json` → `[1].tools[1]` |
| Tools | Modeling & Simulation | LTspice | `assets/toolkit.json` → `[1].tools[2]` |
| Tools | Modeling & Simulation | Proteus | `assets/toolkit.json` → `[1].tools[3]` |
| Tools | Embedded Systems | STM32 / CubeIDE | `assets/toolkit.json` → `[2].tools[0]` |
| Tools | Embedded Systems | ESP32 | `assets/toolkit.json` → `[2].tools[1]` |
| Tools | Embedded Systems | Keil | `assets/toolkit.json` → `[2].tools[2]` |
| Tools | Design & Fabrication | KiCad | `assets/toolkit.json` → `[3].tools[0]` |
| Tools | Design & Fabrication | EAGLE | `assets/toolkit.json` → `[3].tools[1]` |
| Tools | Design & Fabrication | CAD | `assets/toolkit.json` → `[3].tools[2]` |
| Tools | Design & Fabrication | 3D printing | `assets/toolkit.json` → `[3].tools[3]` |
| Tools | Digital Design | VHDL | `assets/toolkit.json` → `[4].tools[0]` |
| Tools | Digital Design | Quartus | `assets/toolkit.json` → `[4].tools[1]` |
| Tools | Digital Design | ModelSim | `assets/toolkit.json` → `[4].tools[2]` |
| Tools | Platforms & Workflow | Linux | `assets/toolkit.json` → `[5].tools[0]` |
| Tools | Platforms & Workflow | Windows | `assets/toolkit.json` → `[5].tools[1]` |
| Tools | Platforms & Workflow | Microsoft Office | `assets/toolkit.json` → `[5].tools[2]` |
| In Progress / Tools & Methods | Methods | TinyML | `assets/learning.json` → `[0].tools[0]` |
| In Progress / Tools & Methods | Programming | Python | `assets/learning.json` → `[1].tools[0]` |
| In Progress / Tools & Methods | Robotics | ROS 2 | `assets/learning.json` → `[2].tools[0]` |
| In Progress / Tools & Methods | Robotics | Gazebo | `assets/learning.json` → `[2].tools[1]` |
| In Progress / Tools & Methods | Design & Fabrication | SolidWorks | `assets/learning.json` → `[3].tools[0]` |
| In Progress / Tools & Methods | Design & Fabrication | Fusion | `assets/learning.json` → `[3].tools[1]` |
| In Progress / Tools & Methods | Embedded Systems | FreeRTOS | `assets/learning.json` → `[4].tools[0]` |
| In Progress / Tools & Methods | Embedded Systems | UART / IÂ²C / SPI / CAN | `assets/learning.json` → `[4].tools[1]` |
| In Progress / Tools & Methods | Platforms & Workflow | Git | `assets/learning.json` → `[5].tools[0]` |
| Interested in Exploring / Tools & Methods | Embedded Systems | Raspberry Pi | `assets/exploring.json` → `[0].tools[0]` |
| Interested in Exploring / Tools & Methods | IoT | MQTT | `assets/exploring.json` → `[1].tools[0]` |
| Interested in Exploring / Tools & Methods | Design & Fabrication | OpenSCAD | `assets/exploring.json` → `[2].tools[0]` |
| In Progress / Areas | AI & Intelligent Systems | Machine Learning | `assets/profile.json` → `learning_area_groups[0].tools[0]`; update matching summary list too |
| In Progress / Areas | Control & Sensing | Embedded & Motor Control | `assets/profile.json` → `learning_area_groups[1].tools[0]`; update matching summary list too |
| In Progress / Areas | Control & Sensing | Sensor Fusion | `assets/profile.json` → `learning_area_groups[1].tools[1]`; update matching summary list too |
| In Progress / Areas | Control & Sensing | System Modelling & Design | `assets/profile.json` → `learning_area_groups[1].tools[2]`; update matching summary list too |
| Interested in Exploring / Areas | Signal Processing | DSP | `assets/profile.json` → `exploring_area_groups[0].tools[0]`; update matching summary list too |
| Interested in Exploring / Areas | Automation | PLC & Automation | `assets/profile.json` → `exploring_area_groups[1].tools[0]`; update matching summary list too |
| Interested in Exploring / Areas | Energy Systems | Renewable Energy | `assets/profile.json` → `exploring_area_groups[2].tools[0]`; update matching summary list too |
| Interested in Exploring / Areas | Energy Systems | HVAC Systems | `assets/profile.json` → `exploring_area_groups[2].tools[1]`; update matching summary list too |
| Interested in Exploring / Areas | Energy Systems | Data Center Design & Operations | `assets/profile.json` → `exploring_area_groups[2].tools[2]`; update matching summary list too |
| Working Areas | Primary | Control Systems | `assets/profile.json` → `areas[0]` |
| Working Areas | Primary | Robotics | `assets/profile.json` → `areas[1]` |
| Working Areas | Supporting | Embedded Systems | `assets/profile.json` → `areas[2]` |
| Working Areas | Supporting | Power Electronics | `assets/profile.json` → `areas[3]` |
| Working Areas | Supporting | Mechatronics | `assets/profile.json` → `areas[4]` |
| Working Areas | Supporting | IoT | `assets/profile.json` → `areas[5]` |
| Working Areas | Supporting | Circuit Design | `assets/profile.json` → `areas[6]` |
| Working Areas | Supporting | 3D Printing | `assets/profile.json` → `areas[7]` |

## 4. Add or move a card

1. Find the destination group in the inventory above.
2. Add the label to its `tools` array. To move a card, remove the original occurrence too.
3. For an area card, update both the grouped array and its flat accessible summary (`learning_areas` or `exploring_areas`).
4. Check the label in `brand-map.json` or `icon-map.json`. A new item must have a deliberate logo/icon mapping; there is no generic fallback.
5. Run `python scripts/test_labels.py`, then rebuild. Check long labels and the mobile layout.

A Tools group has this shape:

```json
{"name": "Programming", "color": "warm", "tools": ["C", "C++", "Assembly"]}
```

Learning/exploration groups and area groups need only `name` and `tools`. The optional `learning` array in a Tools group is metadata, not an automatic transfer between sections. For example, CAD can remain a broad tool entry while SolidWorks and Fusion appear as specific tools in progress.

`labels.py` separates matching from display. `match_key` normalizes Unicode, Turkish character variants, spacing and case for matching. C, C++ and C# remain distinct. `display_label` preserves special spellings such as TinyML, LTspice and ROS 2 while applying title-style capitalization. Add a new special spelling to its spelling table if necessary. Duplicate normalized keys with conflicting mappings fail validation.

## 5. Build locally

From the repository root, use Python 3.12 or newer:

```sh
python -m pip install fonttools pillow
python scripts/build_dashboard.py
python scripts/build_toolkit.py
python scripts/refresh_hero.py
python scripts/build_adaptive.py
python scripts/build_halo_atlas.py
python scripts/build_readme.py
python scripts/build_static.py
```

This uses the saved public snapshot. To fetch fresh public data first, run `python scripts/public_calendar.py` and `python scripts/refresh_public_profile.py`. The full refresh needs an authenticated GitHub CLI or `GH_TOKEN`; CI provides the workflow token. Never export a private-data token for these public statistics.

Run the repository checks:

```sh
python scripts/test_labels.py
python scripts/test_refresh_transport.py
python scripts/test_public_activity.py
python scripts/test_public_calendar.py
python scripts/test_pcb_components.py
python scripts/test_contribution_routing.py
python scripts/test_publish_public_assets.py
python scripts/test_readme_live.py
```

Normal edits reuse embedded robot frames and component PNGs; Blender is unnecessary. For component model changes only:

```sh
blender --background --python scripts/render_pcb_components.py
python scripts/prepare_pcb_components.py
```

Then run the full build/check sequence. `PCB_PART_VARIANTS=2,6` limits rendering/preparation to both capacitor orientations when the existing metadata uses the same camera and render dimensions. Clear the variable afterward. Changing the camera requires all eight renders; otherwise images and metadata disagree. Always prepare from fresh full-canvas renders, not previously cropped PNGs.

## 6. What updates automatically

The workflow fetches an anonymous calendar so its dates, counts and five levels match the public signed-out graph. Repository activity totals are public-only and include repository creation where applicable. Language distribution is computed from eligible public source bytes; it can differ from third-party cards with different filters. Featured cards follow native GitHub pins and fetch multiple repository languages. No view counter is active.

`assets/public-profile.json`, `README.md`, `docs/STATIC.md` and generated SVGs are outputs. `assets/profile.json`, the tool lists, icon/brand maps and scripts are inputs. `.gitattributes` contains `* linguist-vendored` for this repository; the language collector separately excludes the profile repository. This does not change other repositories or force third-party statistics providers to use the same filters.

## 7. Layout and animation rules

Small cards use static colored left accents. Large-card halos use the same eight-second duration on separate SVG resources. The README avoids atlas fragments to preserve WebKit image proportions and reduce Firefox rendering work; image load times can introduce a small phase offset. `card-halos.svg` is retained as a compatibility output; electric sparks belong only to the contribution current. The hand cursor makes an occasional subtle click. Contribution bodies may project over calendar lines while their pads retain clearance; package scales are consistent within each type. The current enters and exits actual terminals and is masked inside bodies.

Both themes share geometry. Theme colors use `prefers-color-scheme`; a browser/host override may affect which scheme is exposed to embedded SVGs. Reduced-motion picture sources select still assets. The footer provides a manual still version; blocked SVG animation is not automatically detectable in GitHub README. SVG text is drawn as vector paths and is not selectable like ordinary Markdown text.

GitHub README does not support custom page JavaScript, sticky robot layers or arbitrary CSS hover layouts. Back to Top is a footer anchor. Do not add inline CSS/JS expecting website behavior. The portfolio is the place for full project descriptions; keep the profile focused on working areas and tools.

## 8. Troubleshooting and rollback

| Symptom | Check |
| --- | --- |
| Edit disappears | You changed an output; edit the input from the source map instead |
| Missing icon | Check normalized mappings and the referenced SVG basename; run label tests |
| Still layout differs | Rebuild both variants; static modules must regenerate their still outputs even without SMIL |
| Counts differ from your signed-in profile | Compare signed-out GitHub first; private contributions are excluded |
| Public Activity differs by one | Check repository creation; do not invent an adjustment |
| New pin missing | Wait for a successful scheduled refresh; inspect public pin visibility and Actions logs |
| Browser shows old art | Check latest successful publication and hashed README URLs; allow proxy caching time |
| CI succeeds but no main update | Branch runs do not publish; check main-run publication step, secret presence and stale-output skip |
| File paths break | Run the commands from the repository root and keep README/static relative paths generated |
| Broken component silhouettes | Rerender all variants if projection changed, prepare fresh renders, run routing/package tests |

For a content rollback, revert the source commit and let the workflow regenerate. Reverting only SVGs is temporary. Do not delete the publication secret or change repository protection just to refresh metrics.

## 9. Browser checks and language options

See [Validation](VALIDATION.md) for the latest engine results, performance caveats and physical-device limits. Run **Actions → Profile browser checks** after layout changes. [Language options](LANGUAGE-OPTIONS.md) evaluates a generated Turkish companion page; no language switch has been added yet.
