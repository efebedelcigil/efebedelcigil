# Profile validation

Last checked: 15 November 2026. The browser checks run against the generated README and assets in a local HTTP fixture with GitHub-like content width. They do not reproduce every part of GitHub's CSS or image proxy.

## Browser and layout checks

[Cross-engine run](https://github.com/efebedelcigil/efebedelcigil/actions/runs/43695382457) passed all 18 scenarios across Chromium, Firefox and WebKit on a Linux runner. Screenshots and `results.json` are attached to the run.

| Scenario | Chromium | Firefox | WebKit |
| --- | --- | --- | --- |
| Desktop dark | Passed | Passed | Passed |
| Desktop light | Passed | Passed | Passed |
| Phone portrait viewport | Passed | Passed | Passed |
| Phone landscape viewport | Passed | Passed | Passed |
| Tablet viewport | Passed | Passed | Passed |
| JavaScript disabled, reduced motion | Passed | Passed | Passed |

Checks include loaded images, no horizontal overflow, reasonable document height, genuine reduced-motion sources and changing hero samples. Phone/tablet rows are viewport tests; Chromium/WebKit also use touch/mobile context settings. Firefox uses the same viewport sizes without pretending to emulate mobile Firefox.

These are **not physical iOS/Android tests**. WebKit on Linux is **not Safari on macOS or iOS**. No attached physical device or real Safari session was available. Hardware-specific performance remains unverified.

## Animation performance

The earlier shared SVG atlas produced a WebKit intrinsic-size problem and made Firefox work harder. The README now embeds independently sized SVG modules. The atlas remains a compatibility output but is not referenced by the current README. Large halos keep their eight-second duration; separate resource load times can introduce a small phase offset.

The initial Firefox sample with the atlas measured approximately 40.5 requestAnimationFrame callbacks per second and a 34.02 ms 95th-percentile interval. A standalone-module comparison measured 60.5 and 17.12 ms. The final run measured:

| Engine | Animated page callbacks/s | 95th-percentile interval | Hero still callbacks/s |
| --- | ---: | ---: | ---: |
| Chromium | 60.5 | 16.7 ms | 60.5 |
| Firefox | 60.5 | 17.1 ms | 60.5 |
| WebKit | 26.5 | 126 ms | 63 |

These short samples are frame-pacing diagnostics, not GPU-level FPS measurements or a device benchmark. Separate runs are subject to runner load. All engines produced distinct hero captures. The robot is authored at 24 frames per second; requestAnimationFrame cadence and decoded animation frame rate are different measurements.

The Firefox issue improved in the tested environment. The Linux software-rendered WebKit sample still shows a cost from the animated hero; replacing only the hero with its still version restored approximately 63 callbacks/s. This does not establish the frame rate on actual Safari. The reduced-motion sources and footer still page provide the existing low-motion option. The robot's accepted movement sequence and image quality were retained instead of silently lowering quality or removing animation.

## General checks

- 40 Python unit tests passed, including content normalization, public activity, calendar parity, transparent component assets, API authentication boundaries, generated README and publication logic.
- Terminal routing passed 64 direction cases, 64 adjacent-package cases, 128 projected neighbor cases, all five homogeneous levels and four seeded mixed calendars.
- The hero checker retained 559 source frames and validated 453 decoded unique frames, identical theme geometry, mobile/desktop variants and the accepted 132-second schedule.
- No private aggregate contribution values or profile view counter were added. The anonymous calendar and public source snapshot remain the data inputs.
- The API transport regression test reproduced the anonymous-auth failure before the fix and verifies that the workflow token is sent only to HTTPS api.github.com requests.

## Repeat the checks

Use the commands in [Editing the profile](PROFILE-EDITING.md). For cross-engine checks, open **Actions → Profile browser checks → Run workflow** on `main`, then inspect the uploaded report and screenshots. This workflow uses read-only repository permissions and does not publish profile changes. Source/data publication remains in **Public profile artwork**.

## PCB surface refinement

[Surface cross-engine run](https://github.com/efebedelcigil/efebedelcigil/actions/runs/43697216876) passed the same 18 scenarios after the softer board palette, decorative trace mask and contact shadows were added. Three surface tests cover empty/dense calendars and exact active-date correspondence. The treatment uses shared radial gradients without new blur filters or animation; component models, sizes and specular lighting are unchanged.
