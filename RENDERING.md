# Render-box workflow

The scene and scripts are coordinated through this Git repository.
Generated frames and videos stay in a separate render-output directory.
The packed scene includes its poster textures and font, so the render box does not need the reference photographs or the Windows font paths used during modeling.

## Linux setup

Install Blender 5.2.1 with `bash scripts/install_blender_linux.sh`.
The installer verifies the archive against Blender's SHA-256 manifest and installs it under `~/.local/opt` without changing system packages.
The render runner also requires Python 3, FFmpeg, FFprobe, and a compatible NVIDIA driver.

## Update and render

Pull changes with `git pull --ff-only` from an existing checkout.
Run the following command from the repository root:

```bash
python3 scripts/render_job.py \
  --blender ~/.local/opt/blender-5.2.1-linux-x64/blender \
  --scene scenes/ref-2-cinematic-pan.blend \
  --output ~/renders/blender-experiment/final
```

Use a new output directory when changing the scene or camera.
The runner resumes files already in that directory, so reusing it for a different revision would mix frames from different renders.

For durable remote execution, run this command inside a tmux or wmux pane.
`pan-progress.json` reports completed frames.
The job then encodes H.264 and checks all 168 frames, 1280 by 720 resolution, 24 fps, seven-second duration, and error-free decoding.
The delivery is `ref-2-cinematic-pan-720p.mp4`, with a checksum and verification details in `pan-verification.json`.

## Verified host

On September 5, 2026, this scene rendered successfully on `homelab` using Blender 5.2.1 and its NVIDIA RTX PRO 6000 Blackwell Workstation Edition.
Three benchmark frames completed in 6.2 seconds including initial setup.
The existing model-serving process remained running during the benchmark and animation render.
The completed seven-second video took 252.6 seconds for rendering, encoding, and verification.
Machine load and scene complexity can change future timings.

## Use both machines

Each machine can render a different, non-overlapping frame range from the same committed scene.
A useful starting allocation is 70% of the frames to homelab and 30% to the local workstation.
This is approximately 1.3 to 1.5 times faster than homelab alone at the observed render speeds, assuming neither machine is busy with another GPU workload.

Start frames 1 through 118 on homelab:

```bash
~/.local/opt/blender-5.2.1-linux-x64/blender \
  --background scenes/ref-2-cinematic-pan.blend \
  --python scripts/render_ref2_pan.py -- \
  --output ~/renders/blender-experiment/split-remote \
  --frame-start 1 --frame-end 118
```

At the same time, start frames 119 through 168 on Windows:

```powershell
$blender = "$env:LOCALAPPDATA\Programs\Blender\blender-5.2.1-windows-x64\blender.exe"
& $blender --background scenes/ref-2-cinematic-pan.blend `
  --python scripts/render_ref2_pan.py -- `
  --output outputs/split-local --frame-start 119 --frame-end 168
```

Copy the remote output folder back to `outputs/split-remote`, including its `render-settings.json` file.
Then collect the two frame sets and encode the finished video:

```bash
python scripts/merge_render_frames.py \
  --source outputs/split-local --source outputs/split-remote \
  --output outputs/split-merged
python scripts/render_job.py --encode-only \
  --scene scenes/ref-2-cinematic-pan.blend --output outputs/split-merged
```

The merge tool rejects different scene hashes, mismatched render settings, conflicting copies of a frame, and incomplete sequences.
The final encoder checks the complete video again.
This workflow uses explicit frame ranges; it does not yet provide automatic load balancing or job scheduling.
