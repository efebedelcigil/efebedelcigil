# Animation ideas

The header combines personal lettering with the original compact cobalt robot on the upper right. A larger PCB and its components are visible in the foreground, and a larger control-response monitor sits on the right. Preserve the robot's materials and stationary station viewpoint. Scanning triangles, projected fills, beams and holograms are cancelled.

## Active interactions

- The button press during the 2.25-second startup triggers the name typing once, with a temporary cursor. The name is complete at 1.8 seconds and does not reset when the robot schedule repeats.
- In a reusable 16-second work clip, the robot picks a chip from the PCB, carries it to the tray and returns it to the PCB. The gripper visibly grasps and releases the component.
- The same work clip includes a slow tuning-knob adjustment and a one-second hold. The monitor's illustrative second-order response spans damping settings from 0.12 to 1 and returns to its steady setting with the knob.
- A separate 5-second glance clip combines physical arm reach with localized depth emphasis on the arm foreground only. The stereo-camera head makes a quick bird-like tilt of about 17 degrees, holds and returns smoothly. The PCB, screen, button and other station props remain fixed. This is a visual greeting, without visitor detection or camera access.
- The underline beneath the name reacts to calibration as part of the same header animation. Other interactions remain in the sequence; the reader glance does not replace them.

The work and glance clips follow a fixed 132-second schedule: `work → glance → work → work → glance → work → glance → work → work → work → glance`. This gives seven work clips and four glances with uneven intervals, not actual randomness. It is an independent robot schedule, not a long introduction; the complete name is already available after startup.

The robot, chip, tray, button, knob, monitor, PCB and lettering share one transparent composition. Light and dark versions use identical geometry. The static version uses a lossless full-scene steady-state PNG with the complete name and steady underline. Animated startup/work foregrounds reuse a shared background. The glance arm is composited over a separate unchanged background containing the steady dial, response graph, chip and all other props. Its localized perspective is calibrated to the fixed shoulder anchor; the station retains its original stationary orthographic projection. This is an artistic layer treatment rather than a single physical camera projection for the whole image. Repeated clips reuse frame IDs rather than embedding a new image set each time.

## Alternatives for later

- An occasional tool inspection or gripper self-test could extend a later sequence.
- The arm could adjust a small name detail through direct contact in a future render; the current underline response is already part of the shared animation.
- A sensor or motor could replace the tuning component when related engineering work is published.
- Catching a loose component could be a rare alternative sequence.

The earlier full-width workbench scene is retained in the source history and renderer. It is not the current README composition. The foreground PCB is part of the approved robot header. No custom contribution widget is displayed; GitHub's native calendar is the activity indicator.

Sticky positioning, scroll reactions and pointer interaction require a separate web page and are outside this README-only version. A voting page was considered but is not part of the delivery.

Build instructions and compatibility limits are in [ANIMATION.md](ANIMATION.md).
