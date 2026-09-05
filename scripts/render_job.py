"""Portable render/encode/verify runner for a workstation or render box."""
import argparse, subprocess, shutil, json, hashlib, time, os
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('--blender',default=os.environ.get('BLENDER_BIN') or shutil.which('blender'))
parser.add_argument('--scene',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
if not args.blender:parser.error('Set --blender or BLENDER_BIN.')
root=Path(__file__).resolve().parents[1];out=args.output.expanduser().resolve();out.mkdir(parents=True,exist_ok=True)
flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
started=time.time()
subprocess.run([args.blender,'--background',str(args.scene.expanduser().resolve()),'--python',str(root/'scripts'/'render_ref2_pan.py'),'--','--output',str(out)],check=True,creationflags=flags)
frames=[out/'pan-final-frames'/f'frame-{f:04d}.png' for f in range(1,169)]
missing=[str(p) for p in frames if not p.exists() or p.stat().st_size<100000]
if missing:raise RuntimeError(f'Missing or incomplete frames: {missing}')
video=out/'ref-2-cinematic-pan-720p.mp4'
subprocess.run(['ffmpeg','-hide_banner','-y','-framerate','24','-start_number','1','-i',str(out/'pan-final-frames'/'frame-%04d.png'),'-frames:v','168','-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(video)],check=True,creationflags=flags)
probe=subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=codec_name,width,height,r_frame_rate,nb_read_frames,duration,pix_fmt','-of','json',str(video)],capture_output=True,text=True,check=True,creationflags=flags)
evidence=json.loads(probe.stdout);s=evidence['streams'][0]
assert (s['width'],s['height'],s['nb_read_frames'],s['r_frame_rate'])==(1280,720,'168','24/1')
assert abs(float(s['duration'])-7)<.01
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True,creationflags=flags)
evidence.update({'file':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'bytes':video.stat().st_size,'elapsed_seconds':round(time.time()-started,1),'decode_check':'passed'})
(out/'pan-verification.json').write_text(json.dumps(evidence,indent=2))
print('RENDER JOB COMPLETE',json.dumps(evidence),flush=True)
