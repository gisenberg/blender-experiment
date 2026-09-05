"""Safely collect disjoint frame sets rendered by multiple machines."""
import argparse, hashlib, json, shutil
from pathlib import Path

def merge_frames(sources, target, allow_incomplete=False):
    settings=None
    for source in sources:
        incoming=json.loads((source/'render-settings.json').read_text())
        if settings is None:settings=incoming
        elif incoming!=settings:raise ValueError('Workers rendered different scenes or settings.')
    target.mkdir(parents=True,exist_ok=True)
    marker=target/'render-settings.json'
    if marker.exists() and json.loads(marker.read_text())!=settings:raise ValueError('Target belongs to a different render job.')
    marker.write_text(json.dumps(settings,indent=2))
    destination=target/'pan-final-frames';destination.mkdir(exist_ok=True)
    for source in sources:
        for frame in sorted((source/'pan-final-frames').glob('frame-*.png')):
            dest=destination/frame.name
            if dest.exists():
                if hashlib.sha256(dest.read_bytes()).digest()!=hashlib.sha256(frame.read_bytes()).digest():raise ValueError(f'Conflicting copies of {frame.name}')
            else:
                temporary=dest.with_suffix('.png.partial');shutil.copyfile(frame,temporary);temporary.replace(dest)
    missing=[f for f in range(settings['frame_start'],settings['frame_end']+1) if not (destination/f'frame-{f:04d}.png').exists()]
    if missing and not allow_incomplete:raise ValueError(f'Missing {len(missing)} frames; first missing frame: {missing[0]}')
    return {'frames':settings['frame_end']-settings['frame_start']+1-len(missing),'missing':missing,'output':str(target)}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,action='append',required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--allow-incomplete',action='store_true')
    args=parser.parse_args();print(json.dumps(merge_frames(args.source,args.output,args.allow_incomplete),indent=2))
