"""Create a seven-second, gently eased dolly-pan without replacing the still project."""
import bpy, os, math
from mathutils import Vector
scene=bpy.data.scenes['Ref 2 - Abandoned underground concourse'];bpy.context.window.scene=scene
out=os.path.dirname(bpy.data.filepath)
original=scene.camera
camera=original.copy();camera.data=original.data.copy();camera.name='Cinema camera - slow dolly and pan';scene.collection.objects.link(camera);scene.camera=camera
camera.rotation_mode='QUATERNION';camera.data.lens=23
scene.frame_start=1;scene.frame_end=168;scene.render.fps=24
start=Vector((3.95,-7.05,1.40));end=Vector((2.70,-5.90,1.38))
look_start=Vector((-3.10,3.6,.34));look_end=Vector((-.35,4.0,.36))
for f in range(1,169):
    t=(f-1)/167
    # Smooth acceleration and deceleration with no handheld wobble.
    t=t*t*(3-2*t)
    camera.location=start.lerp(end,t)
    target=look_start.lerp(look_end,t)
    camera.rotation_quaternion=(target-camera.location).to_track_quat('-Z','Y')
    camera.keyframe_insert(data_path='location',frame=f)
    camera.keyframe_insert(data_path='rotation_quaternion',frame=f)
scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
scene.render.use_persistent_data=True
scene.cycles.samples=128;scene.cycles.use_adaptive_sampling=True;scene.cycles.adaptive_threshold=.015;scene.cycles.adaptive_min_samples=32
scene.cycles.use_denoising=True;scene.cycles.use_animated_seed=False
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='8';scene.render.image_settings.compression=20
os.makedirs(os.path.join(out,'pan-720-7s-frames'),exist_ok=True)
scene.render.filepath=os.path.join(out,'pan-720-7s-frames','frame-')
scene['animation_description']='7 seconds at 24 fps: eased lateral dolly with a slow rightward pan across the underground concourse.'
scene.frame_set(84)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out,'ref-2-cinematic-pan.blend'))
result={'file':bpy.data.filepath,'frames':168,'fps':24,'samples':128}
