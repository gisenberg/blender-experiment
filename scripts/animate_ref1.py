import bpy,os
from mathutils import Vector
s=bpy.context.scene;original=s.camera;c=original.copy();c.data=original.data.copy();c.name='R1 | Cinematic seven-second camera';s.collection.objects.link(c);s.camera=c;c.rotation_mode='QUATERNION';c.animation_data_clear()
s.frame_start=1;s.frame_end=168;s.render.fps=24
for f in range(1,169):
    t=(f-1)/167;t=t*t*(3-2*t)
    c.location=Vector((13.5,-22,8.2)).lerp(Vector((11.6,-20.6,7.8)),t)
    target=Vector((-1,6,1.2)).lerp(Vector((1,6,1.0)),t)
    c.rotation_quaternion=(target-c.location).to_track_quat('-Z','Y')
    c.keyframe_insert(data_path='location',frame=f);c.keyframe_insert(data_path='rotation_quaternion',frame=f)
s.frame_set(84);s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.cycles.samples=64;s.cycles.use_adaptive_sampling=True;s.cycles.adaptive_min_samples=16;s.cycles.adaptive_threshold=.025;s.cycles.use_denoising=True;s.cycles.use_animated_seed=False;s.render.use_persistent_data=True
s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=20
s['animation_description']='Seven-second eased elevated dolly and rightward pan through the hazy abandoned service yard.'
s.render.filepath=os.path.join(os.path.dirname(bpy.data.filepath),'distributed','pan-final-frames','frame-')
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.dirname(bpy.data.filepath),'ref-1-cinematic-pan.blend'))
result={'scene':s.name,'file':bpy.data.filepath,'frames':s.frame_end}
