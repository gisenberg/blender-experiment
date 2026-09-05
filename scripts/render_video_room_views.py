"""Render the reconstruction and its two reference-oriented cameras."""
import bpy
from pathlib import Path
s=bpy.context.scene
out=Path(bpy.data.filepath).parent
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
s.cycles.device='GPU';s.render.resolution_percentage=100;s.cycles.samples=128
for name,filename in [
    ('Music room - reconstructed wide view','music-room-still.png'),
    ('Music room - frontal source angle','music-room-frontal.png'),
    ('Music room - keyboard source angle','music-room-keyboard.png'),
]:
    s.camera=bpy.data.objects[name]
    s.render.filepath=str(out/filename)
    bpy.ops.render.render(write_still=True)
print('ALL ROOM VIEWS COMPLETE',flush=True)
