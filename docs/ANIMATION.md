# Profile hero

The README opens with one transparent composition: outlined Bricolage Grotesque lettering on the left and a compact cobalt robot on the upper right. The robot keeps the approved design, materials and viewpoint. A larger PCB and its components sit visibly in the foreground on a fixture; the control-response monitor is on the right. There are no scanning triangles, scan fills, projected beams or holograms. The original separate name banner, gyroscope and full-width workbench are no longer used in the README.

## Timing

A short startup sequence lowers the gripper onto the control button. The name appears character by character from left to right, with a temporary block cursor, and finishes at 1.8 seconds. The startup lasts 2.25 seconds; the name is then complete while the robot begins its independent repeating schedule. There is no 132-second introduction or wait to use the profile. The clock starts when the image is ready to animate; network and image-decoding time are additional.

The robot reuses a 16-second work clip and a separate 5-second glance clip. Its 132-second schedule is:

`work → glance → work → work → glance → work → glance → work → work → work → glance`

This is seven work clips and four glances. The gaps between glances vary because of this fixed schedule; they are not actually random. The name does not reset when the schedule repeats.

SVG declarative animation drives the two timelines. There is no client-side JavaScript, WebGL engine, pointer tracking or camera access. Reloading the image or selecting another theme can create a new image instance and replay its startup.

The repeating sequence preserves several physical interactions:

- The gripper picks up a chip from the foreground PCB, carries it to the tray, releases it, then picks it up and returns it to the PCB. This is a visible component transfer rather than an empty-gripper inspection.
- The gripper approaches, grasps and slowly rotates the tuning knob. The monitor displays an illustrative second-order response whose damping changes from 0.12 to 1 as the knob is adjusted.
- During the separate glance clip, the physical arm reaches toward the reader and receives localized depth emphasis in its own foreground layer. The stereo-camera head makes a quick inquisitive tilt of about 17 degrees, holds and returns smoothly. The station, PCB, screen and button keep their fixed projection and framing. This is a rendered gesture, without visitor detection or camera access.
- The underline beneath the name responds to calibration within the shared header animation. The name remains complete while this smaller response repeats.

The robot uses spatial inverse kinematics, fifth-order motion easing and a compensating wrist. A lateral elbow shaft separates the two arm shells; the startup button sits on an extension in front of the base. In the reusable source timeline, the knob turns from +0.75 to −0.85 radians during 13.00–14.25 seconds, holds for one second, and restores during 15.25–16.40 seconds while the gripper remains in contact. These are source-clip times, not new delays imposed on every page visit. The monitor shows an illustrative response, not a measured project result. No custom contribution statistics are displayed; GitHub's native contribution calendar remains the profile's activity indicator.

The station uses the original stationary orthographic projection. For the glance, only the arm foreground uses a depth/perspective treatment calibrated to the fixed shoulder anchor. It is composited over an unchanged background containing the steady dial, response graph, chip and other props. This is an artistic layered composition, not a single-camera physical projection of the entire scene. A lens change in that foreground render affects only the arm; there is no whole-scene zoom or movement of the PCB, screen or button.

## Static state and compatibility

The static hero contains the complete name, no typing cursor, a steady underline and a lossless full-scene steady-state PNG. The foreground PCB and right-hand monitor remain visible. The same composition and letter outlines are used in the animated hero. Light/dark variants change text/accent colors only; the robot frames and geometry are identical.

Reduced-motion preferences select a nonanimated SVG with the lossless full-scene PNG. Outer PNG sources provide the image-format fallback, and the explicit Still version offers a completely static README. The animated hero embeds individual still WebP frames with transparency; SVG SMIL switches their referenced IDs at 24 fps. Startup and work foregrounds are layered over one shared static background to save bytes. The glance reuses a separate unchanged station background, with only its arm foreground animated and given localized depth emphasis. There is no nested animated WebP or external frame request. If the embedded images decode but declarative SVG animation is unavailable, the unanimated defaults contain the full name and steady robot pose. The outer image-format fallback cannot detect unsupported WebP decoding inside an otherwise supported SVG; use the explicit Still version in that case.

The source sequence has 559 rendered frames at 24 fps, including a closing boundary frame. The animation tracks use 54 intro frames, 384 work frames and 120 glance frames. The 132-second schedule reuses those clip IDs rather than embedding extra image sets for every repetition; identical raster frames are stored once. The builder targets a 9.9 MB budget per selected animated SVG; final quality and measured build sizes are recorded in `.render/hero-build.json` after rebuilding. Only the selected picture source loads. This trades a larger image payload for synchronized native GitHub animation without a runtime engine. Firefox/WebKit and physical-device rendering have not been tested.

GitHub strips positioning CSS, so this is an upper-right composition inside the header image, not a sticky object that follows the browser viewport.

## Rebuild

Use Blender 4.5 LTS, Python with Pillow and fontTools, and Node with the dependency in package.json. The font and OFL license are bundled in assets/fonts; visitors need no installed font.

```sh
python -m pip install pillow fonttools
npm install
blender --background --python scripts/render_portrait.py -- --out /absolute/path/to/repo/.render/portrait --layered
python scripts/build_hero.py
npm run posters
python scripts/build_toolkit.py
python scripts/build_static.py
```

The builder reads source frames from `.render/portrait`. The required `--layered` render also writes `.render/portrait-background.png`, `.render/portrait-glance-background.png` and `.render/portrait-steady.png` beside that directory. The glance background contains the stationary props in their steady state. Preserve all three background and steady-state files when rebuilding. The original workbench renderer is retained as the procedural model source and can generate the earlier engineering scene independently. Its dated activity snapshot is not used in the profile hero.

After changing the motion or composition, regenerate the affected source frames before rebuilding the hero, posters and static README. Do not package or publish a header built from an earlier render: asset checks must apply to the final rendered sequence.

## Verification

```sh
python scripts/check_hero.py
blender --background --python scripts/check_portrait.py
```

The asset check validates every source frame, every embedded raster, all local references, theme geometry, animation tracks, single-play name reveal and static defaults. The motion check samples 2,791 states at 120 Hz. Its source-clip joins at 2.25, 18.25 and 23.25 seconds have zero checked state error, allowing the work and glance clips to be reused in the schedule. It checks 30 nonadjacent shell pairs for surface intersections in all 559 source frames, including the chip, foreground PCB, monitor, camera, flange and gripper. Chip-transfer transitions are checked for positional continuity. The two illustrative damping settings produce a graph-peak difference of approximately 0.1505 scene units. The check also verifies that the PCB is visible and the scan objects are hidden. Intentional joints and button contact are excluded. These are scoped kinematic and visual checks, not a physics simulation, a complete collision model or hardware certification.

The projection check confirms a fixed station and a shoulder-anchor error below 0.000006 in normalized screen coordinates. The background layers are shared lossless images. Repeat both projection and compositing checks after camera or render changes.
