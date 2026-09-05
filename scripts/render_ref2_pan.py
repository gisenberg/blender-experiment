"""Resumable PNG animation render. Use --checks for framing verification."""
import bpy, os, sys, time, json
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--output');parser.add_argument('--frames');parser.add_argument('--checks',action='store_true')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
scene=bpy.data.scenes['Ref 2 - Abandoned underground concourse'];bpy.context.window.scene=scene
out=os.path.abspath(os.path.expanduser(args.output)) if args.output else os.path.dirname(bpy.data.filepath)
os.makedirs(out,exist_ok=True)
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU';scene.render.use_persistent_data=True
checks=args.checks
frames=[scene.frame_start,(scene.frame_start+scene.frame_end)//2,scene.frame_end] if checks else range(scene.frame_start,scene.frame_end+1)
if args.frames:frames=[int(v) for v in args.frames.split(',')]
folder=os.path.join(out,'pan-final-frames')
if checks:folder+='-checks'
os.makedirs(folder,exist_ok=True)
started=time.time()
print('RENDER CONFIG',json.dumps({'version':bpy.app.version_string,'gpu':[d.name for d in prefs.devices if d.use],'resolution':[scene.render.resolution_x,scene.render.resolution_y],'samples':scene.cycles.samples,'output':out}),flush=True)
for frame in frames:
    path=os.path.join(folder,'frame-%04d.png'%frame)
    if os.path.exists(path) and os.path.getsize(path)>100000:
        print('SKIP frame',frame,flush=True);continue
    scene.frame_set(frame);scene.render.filepath=path
    bpy.ops.render.render(write_still=True)
    with open(os.path.join(out,'pan-progress.json'),'w') as f:json.dump({'frame':frame,'total':scene.frame_end,'checks':checks,'elapsed_seconds':round(time.time()-started,1)},f)
    print('FINISHED frame',frame,'elapsed',round(time.time()-started,1),flush=True)
print('ALL REQUESTED FRAMES COMPLETE',flush=True)
