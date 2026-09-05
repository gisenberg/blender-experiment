"""Compatibility entry point for the generic resumable frame renderer."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('render_frames.py')),run_name='__main__')
