"""Run the durable animation job, encode an MP4, and verify the delivery."""
from pathlib import Path
import subprocess, shutil, json, hashlib, time
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs'/'ref-2'
BLENDER=Path(r'C:\Users\gisen\AppData\Local\Programs\Blender\blender-5.2.1-windows-x64\blender.exe')
started=time.time()
for source in (OUT/'pan-final-frames-checks').glob('frame-*.png'):
    shutil.copy2(source,OUT/'pan-final-frames'/source.name)
with (OUT/'pan-render.log').open('w',encoding='utf-8') as log:
    subprocess.run([str(BLENDER),'--background',str(OUT/'ref-2-cinematic-pan.blend'),'--python',str(ROOT/'scripts'/'render_ref2_pan.py')],stdout=log,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
frames=[OUT/'pan-final-frames'/('frame-%04d.png'%i) for i in range(1,169)]
missing=[str(p) for p in frames if not p.exists() or p.stat().st_size<100000]
if missing:raise RuntimeError('Incomplete frame sequence: '+str(missing))
video=OUT/'ref-2-cinematic-pan-720p.mp4'
with (OUT/'pan-encode.log').open('w',encoding='utf-8') as log:
    subprocess.run(['ffmpeg','-hide_banner','-y','-framerate','24','-start_number','1','-i',str(OUT/'pan-final-frames'/'frame-%04d.png'),'-frames:v','168','-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709','-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart','-metadata','title=Abandoned Concourse - Slow Dolly and Pan',str(video)],stdout=log,stderr=subprocess.STDOUT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
probe=subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=codec_name,width,height,r_frame_rate,nb_read_frames,duration,pix_fmt','-of','json',str(video)],capture_output=True,text=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
evidence=json.loads(probe.stdout);stream=evidence['streams'][0]
assert stream['width']==1280 and stream['height']==720
assert stream['nb_read_frames']=='168' and stream['r_frame_rate']=='24/1'
assert abs(float(stream['duration'])-7)<.01
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','NUL'],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
evidence.update({'file':str(video),'bytes':video.stat().st_size,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'elapsed_seconds':round(time.time()-started,1),'decode_check':'passed','frame_sequence_complete':True})
(OUT/'pan-verification.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
print(json.dumps(evidence,indent=2),flush=True)
