"""Render the active scene in a saved Blender project."""
import bpy,sys,argparse
parser=argparse.ArgumentParser();parser.add_argument('--output');parser.add_argument('--percentage',type=int,default=50);parser.add_argument('--samples',type=int,default=64)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
s=bpy.context.scene;prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
s.cycles.device='GPU';s.cycles.samples=args.samples;s.render.resolution_percentage=args.percentage
if args.output:s.render.filepath=args.output
bpy.ops.render.render(write_still=True)
