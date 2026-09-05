# Blender experiment

Blender 5.2.1 LTS and the [official Blender Lab MCP integration](https://www.blender.org/lab/mcp-server/) are installed on this machine.

## Reconstructed concourse and cinematic pan

The packed, editable scene is [scenes/ref-2-cinematic-pan.blend](scenes/ref-2-cinematic-pan.blend).
It contains the abandoned underground concourse, procedural materials, packed poster graphics, lighting, subtle volumetric haze, and an eased camera move.
The animation is 7 seconds at 24 fps, rendered at 1280 by 720 pixels with Cycles and OptiX.
The original reference photographs and generated frame sequences are kept out of Git.

Blender 5.2.1 is required to match the scene's node setup.
With Blender, Python 3, FFmpeg, and an NVIDIA GPU available, render and encode the complete video using:

```bash
python3 scripts/render_job.py \
  --blender /path/to/blender \
  --scene scenes/ref-2-cinematic-pan.blend \
  --output ~/renders/blender-experiment/ref-2
```

The job resumes existing frames and verifies the finished MP4's resolution, frame count, duration, and decoding.
The output directory contains `ref-2-cinematic-pan-720p.mp4`, `pan-verification.json`, and the lossless frame sequence.
See [RENDERING.md](RENDERING.md) for portable Linux installation and the reusable render-box workflow.
For a short machine benchmark, run:

```bash
/path/to/blender --background scenes/ref-2-cinematic-pan.blend \
  --python scripts/render_ref2_pan.py -- \
  --output ~/renders/blender-experiment/benchmark --frames 84,85,86
```

## Reconstructed service yard

The second reconstruction is [scenes/ref-1-cinematic-pan.blend](scenes/ref-1-cinematic-pan.blend).
It contains the prefab workshops, exterior steel stairs, blue rubble skip and trailer, abandoned vehicles, scattered debris, surrounding apartments, procedural weathering, and subtle atmospheric haze.
Its eased camera move is also seven seconds at 24 fps and 1280 by 720 pixels.
Use the same render command above with this scene path and a separate output directory.
The generic worker script is `scripts/render_frames.py`; the older `render_ref2_pan.py` name remains a compatibility wrapper.

The local still is `outputs/ref-1/ref-1-still.png`, and the still-camera project is `outputs/ref-1/ref-1-reconstruction.blend`.
The construction scripts run in Blender in this order: `build_ref1.py`, `refine_ref1.py`, `polish_ref1.py`, `finish_ref1.py`, and `animate_ref1.py`.

## Local integration

1. Open **Blender 5.2** from the Windows Start Menu.
2. Start a fresh Codex session in this project so it loads the project-local `blender` MCP server.
3. Ask Codex to inspect or modify the open Blender scene.

Example: "Use Blender MCP to create a low-poly island with a lighthouse, then save it in this workspace."

The MCP add-on starts automatically with Blender and listens on `127.0.0.1:9876`.
Its settings are under **Edit > Preferences > Add-ons > MCP**.
Blender online access is enabled because the official add-on requires it, including for localhost.
Keep one Blender instance open for this connection.

## Installation details

- Blender: `C:\Users\gisen\AppData\Local\Programs\Blender\blender-5.2.1-windows-x64\blender.exe`.
- Official source: `.tools/blender-lab-mcp`, revision `4309a39646e644261624bfcd2bca669b343b7621`.
- Installed extension: `bl_ext.user_default.mcp`, version 1.0.0.
- Dedicated server environment: `.tools/blender-mcp-venv`, Python 3.11.14.
- MCP SDK: 1.29.1, constrained below 2 because the official server still imports `FastMCP`.
- Codex registration: `blender` in this project's `.codex/config.toml`, with no user-level registration.
- Verified dependency snapshot: `.tools/requirements-verified.txt`.

The server uses this workspace's `.tools` directory, so retain it while the integration is configured.
The MSI could not install under Program Files; the portable ZIP was extracted under the user account instead.
Its SHA-256 matched the release checksum: `0e631dad7d0cad6d5d18abdd2e2550f6c0213215334eda00ddbd3d22b96ecb2c`.

## Verify

With Blender open, run:

```powershell
.tools/blender-mcp-venv/Scripts/python.exe scripts/verify_mcp.py
```

Verification initializes the actual stdio MCP server, discovers 26 tools, inspects the scene, creates/moves/removes a temporary object, and captures the Blender window.
Results are written under `outputs/`.
The connection was verified on September 5, 2026.
