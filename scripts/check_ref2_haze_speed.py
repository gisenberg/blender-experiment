import bpy,os,time
s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
s.cycles.device='GPU';s.render.use_persistent_data=True
folder=os.path.join(os.path.dirname(bpy.data.filepath),'pan-final-frames');os.makedirs(folder,exist_ok=True)
for frame in [5,6,84]:
    start=time.time();s.frame_set(frame);s.render.filepath=os.path.join(folder,'frame-%04d.png'%frame);bpy.ops.render.render(write_still=True)
    print('BENCHMARK',frame,round(time.time()-start,3),flush=True)
