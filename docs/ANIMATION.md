# Workbench animation

A 12-second transparent animation combines a small robot arm, a tuning dial, an EVB name tile, a component tray, a PCB and a feedback display.

## Motion

The arm turns the dial and the displayed response settles toward a reference. It then aligns the name tile, picks up a component, seats it on the board and returns it to the tray. After seating the component, the arm brings its inspection camera forward, briefly turns toward the viewer and shows a small triangular scan before returning to the board. The acknowledgement happens once per loop; it does not detect visitors, access a camera or respond to pointer movement. All objects return to their starting state before the loop repeats.

The arm uses planar inverse kinematics with a vertical gripper axis. Fifth-order easing gives each move zero endpoint velocity and acceleration. It is a precomputed animation, not a real-time physics simulation. The display is an illustrative response, not a measured project result.

The PCB's 28 pads use activity levels from the public GitHub contribution calendar. The source, dates and refresh date are recorded in `assets/workbench-data.json`. The robot's placement cycle is illustrative; placing a component does not claim a new contribution occurred.

## Display and performance

- The desktop and mobile scenes have separate compositions.
- Light and dark variants change the name and subtitle colors. The surrounding background remains transparent.
- A picture element selects one variant. The page does not download a 3D engine or run the renderer.
- Each animation is rendered from 180 frames at 15 fps; identical frames are merged during encoding. The duration stays 12 seconds. Name and profile content are visible from the first frame.
- Reduced-motion preferences select a static WebP instead of the animation. Browsers without WebP support receive a transparent PNG. The Still version link opens an explicitly static README.
- The README contains no scripts. Blocking JavaScript does not hide its content or disable image playback.

## Rebuild

Use Blender 4.5 LTS and Python with Pillow installed. The renderer uses a local Trebuchet font when available and Blender's bundled font otherwise. No font file is distributed.

```sh
python scripts/build_workbench.py --blender /path/to/blender --refresh
```

The refresh step reads only the public contribution calendar. If its format changes or fewer than 28 valid days are available, it fails without replacing the existing snapshot. Temporary frames are stored in the ignored `.render` directory.

Toolkit labels are maintained in `assets/toolkit.json`. To regenerate its four transparent SVG variants:

```sh
python scripts/build_toolkit.py
```

The toolkit builder synchronizes its README alternative text. After editing the README, run `python scripts/build_static.py` to update the static edition. Learning levels remain manually maintained. New engineering work can be added independently using the maintenance guide.

## Contribution privacy and alignment

Private contributions are disabled in the account's native GitHub contribution settings (verified 2026-11-08). Keep that setting off: GitHub can include anonymized private activity in its public calendar when it is enabled.

The refresh script makes an unauthenticated request without cookies or a token. It never queries private repositories. Each PCB pad represents one day's contribution intensity from the same public calendar as GitHub, with 28 dates in chronological order. These are contributions, not a separate commit total. No repository names, counts or private activity are stored.

The board is a dated snapshot, not a live counter. GitHub's native calendar remains authoritative as new activity arrives. Rebuilding with `--refresh` updates all four animations together; changing the JSON alone does not update rendered images.
