"""Render the researched chapel and geometry detail views."""
import bpy
from pathlib import Path
s=bpy.context.scene;out=Path(__file__).resolve().parents[1]/'outputs'/'polyphia-room'
out.mkdir(parents=True,exist_ok=True)
p=bpy.context.preferences.addons['cycles'].preferences;p.compute_device_type='OPTIX';p.get_devices()
for d in p.devices:d.use=d.type=='OPTIX'
s.cycles.device='GPU';s.cycles.use_denoising=True;s.cycles.samples=128;s.render.resolution_percentage=100
light=bpy.data.lights.new('Temporary neutral geometry inspection light','AREA');light.energy=70;light.shape='DISK';light.size=1.5
lamp=bpy.data.objects.new('Temporary neutral geometry inspection light',light);s.collection.objects.link(lamp);lamp.hide_render=True
for name,file in [('São Francisco - revised frame 8 camera','gilded-chapel-refined-still.png'),('São Francisco - scanned statue detail','refined-statue-detail.png'),('São Francisco - carving panel detail','refined-carving-detail.png')]:
    s.camera=bpy.data.objects[name];s.render.filepath=str(out/file)
    lamp.hide_render='revised frame' in name
    lamp.location=s.camera.location;lamp.rotation_euler=s.camera.rotation_euler
    bpy.ops.render.render(write_still=True)
print('REFINED CHAPEL VIEWS COMPLETE',flush=True)
