"""Portable render/encode/verify runner for a workstation or render box."""
import argparse, subprocess, shutil, json, hashlib, time, os
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('--blender',default=os.environ.get('BLENDER_BIN') or shutil.which('blender'))
parser.add_argument('--scene',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--encode-only',action='store_true',help='Encode and verify frames collected from multiple workers.')
parser.add_argument('--name',help='Optional output basename without extension.')
args=parser.parse_args()
if not args.blender and not args.encode_only:parser.error('Set --blender or BLENDER_BIN.')
root=Path(__file__).resolve().parents[1];out=args.output.expanduser().resolve();out.mkdir(parents=True,exist_ok=True)
flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
started=time.time()
if not args.encode_only:
    subprocess.run([args.blender,'--background',str(args.scene.expanduser().resolve()),'--python',str(root/'scripts'/'render_frames.py'),'--','--output',str(out)],check=True,creationflags=flags)
settings=json.loads((out/'render-settings.json').read_text())
if hashlib.sha256(args.scene.read_bytes()).hexdigest()!=settings['scene_sha256']:raise RuntimeError('Scene file does not match the collected frames.')
first=settings['frame_start'];count=settings['frame_end']-first+1;fps=settings['fps']
width=round(settings['width']*settings['percentage']/100);height=round(settings['height']*settings['percentage']/100)
frames=[out/'pan-final-frames'/f'frame-{f:04d}.png' for f in range(first,first+count)]
missing=[str(p) for p in frames if not p.exists() or p.stat().st_size<100000]
if missing:raise RuntimeError(f'Missing or incomplete frames: {missing}')
final_video=out/((args.name or args.scene.stem+f'-{height}p')+'.mp4')
video=final_video.with_name(final_video.stem+'.partial.mp4')
subprocess.run(['ffmpeg','-hide_banner','-y','-framerate',str(fps),'-start_number',str(first),'-i',str(out/'pan-final-frames'/'frame-%04d.png'),'-frames:v',str(count),'-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(video)],check=True,creationflags=flags)
probe=subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=codec_name,width,height,r_frame_rate,nb_read_frames,duration,pix_fmt','-of','json',str(video)],capture_output=True,text=True,check=True,creationflags=flags)
evidence=json.loads(probe.stdout);s=evidence['streams'][0]
assert (s['width'],s['height'],s['nb_read_frames'],s['r_frame_rate'])==(width,height,str(count),f'{fps}/1')
assert abs(float(s['duration'])-count/fps)<.01
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True,creationflags=flags)
video.replace(final_video);video=final_video
evidence.update({'file':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'bytes':video.stat().st_size,'elapsed_seconds':round(time.time()-started,1),'decode_check':'passed'})
(out/'pan-verification.json').write_text(json.dumps(evidence,indent=2))
print('RENDER JOB COMPLETE',json.dumps(evidence),flush=True)
