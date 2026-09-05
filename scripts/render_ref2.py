"""Render the saved reconstruction in a background Blender process."""
import bpy, os, sys
scene=bpy.data.scenes['Ref 2 - Abandoned underground concourse']
bpy.context.window.scene=scene
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU'
if '--final' in sys.argv:
    scene.render.resolution_percentage=100
    scene.cycles.samples=256
    scene.render.filepath=os.path.join(os.path.dirname(bpy.data.filepath),'ref-2-render.png')
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
bpy.ops.render.render(write_still=True)
