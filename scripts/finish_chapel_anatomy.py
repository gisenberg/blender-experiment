"""Refine the reference sculpture using CC0 anatomical targets and skin weights."""
import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from scene_helpers import SceneBuilder
s=bpy.context.scene;b=SceneBuilder.__new__(SceneBuilder);b.scene=s;b.prefix='REFINED';b.cache={};b.collections={}
b.group('Corrected Cristo Serafico anatomy and six feathered wings')
def getmat(part):return next(m for m in bpy.data.materials if part in m.name)
flesh=getmat('Aged polychrome sculpture flesh');hair=getmat('Dark carved hair');ivory=getmat('Ivory carved loincloth');wing=getmat('Old gold feather polychrome');gold=bpy.data.materials['Chapel | Polished raised gilding']
vs=[];faces=[];groups={};g=''
for line in (ROOT/'assets/statues/makehuman-base.obj').read_text().splitlines():
    if line.startswith('v '):vs.append(Vector(tuple(map(float,line.split()[1:4]))))
    elif line.startswith('g '):g=line[2:];groups.setdefault(g,[])
    elif line.startswith('f '):
        f=[int(x.split('/')[0])-1 for x in line.split()[1:]];groups.setdefault(g,[]).extend(f)
        if g=='body':faces.append(f)
for filename,strength in [('male-young.target',1.0),('male-lean-muscle.target',.8)]:
    for line in (ROOT/'assets/statues'/filename).read_text().splitlines():
        if not line or line.startswith('#'):continue
        a=line.split()
        if len(a)==4:vs[int(a[0])]+=Vector(tuple(map(float,a[1:])))*strength
weights=json.loads((ROOT/'assets/statues/makehuman-weights.mhw').read_text())['weights']
arms={'L':{},'R':{}}
for name,pairs in weights.items():
    if name.startswith(('upperarm','lowerarm','wrist','finger','metacarpal')):
        side=name[-1]
        for i,w in pairs:arms[side][i]=arms[side].get(i,0)+w
def joint(name):
    ids=set(groups[name]);return sum((vs[i] for i in ids),Vector())/len(ids)
used=sorted(set(i for f in faces for i in f));index={i:k for k,i in enumerate(used)}
bottom=min(vs[i].y for i in used);top=max(vs[i].y for i in used);H=top-bottom
verts=[]
for idx in used:
    v=vs[idx].copy();original=v.copy()
    for side,sign in [('L',1),('R',-1)]:
        w=arms[side].get(idx,0)
        if w:
            origin=joint('joint-l-shoulder' if side=='L' else 'joint-r-shoulder')
            rotated=origin+Matrix.Rotation(math.radians(64)*sign,3,'Z')@(original-origin)
            v+=(rotated-original)*w
    if v.y<.6:v.x*=1-.77*max(0,min(1,(.6-v.y)/7.6))
    if v.y>6.0:
        origin=joint('joint-neck');w=max(0,min(1,(v.y-6.0)/.8));v=origin+Matrix.Rotation(math.radians(12)*w,3,'X')@Matrix.Rotation(math.radians(9)*w,3,'Z')@(v-origin)
    verts.append((v.x/H*2.02,-v.z/H*2.02,(v.y-bottom)/H*2.02))
body=next(o for o in s.objects if 'Cristo Serafico anatomical body' in o.name)
m=bpy.data.meshes.new('CC0 male anatomical mesh with weighted cruciform pose');m.from_pydata(verts,[],[[index[i] for i in f] for f in faces]);m.materials.append(flesh)
for p in m.polygons:p.use_smooth=True
body.data=m
# Fit drapery to the actual pelvis and upper thigh after the anatomical target changes.
pelvis_height=5.03+(joint('joint-pelvis').y-bottom)/H*2.02
for o in s.objects:
    if 'Gathered ivory loincloth' in o.name or 'Carved hanging cloth fold' in o.name:o.location.z+=pelvis_height+.09-5.94
    if any(t in o.name for t in ['Layered carved flight feather','Feather central quill']):o.hide_render=True;o.hide_viewport=True
# Feather ribbons have individually offset roots, softly rounded vanes, and carved quills.
def feather(a,c,width):
    a=Vector(a);c=Vector(c);d=c-a;side=Vector((d.z,0,-d.x)).normalized();verts=[];N=20
    for i in range(N):
        t=i/(N-1);mid=a.lerp(c,t);w=width*(math.sin(math.pi*t)**.55)
        for j in range(5):
            q=j/2-1;verts.append(tuple(mid+side*w*q+Vector((0,-.009*math.sin(math.pi*t)*(1-.8*abs(q)),0))))
    o=b.mesh('Individually layered flight feather',verts,[(i*5+j,i*5+j+1,(i+1)*5+j+1,(i+1)*5+j) for i in range(N-1) for j in range(4)],wing)
    for p in o.data.polygons:p.use_smooth=True
    b.pipe('Fine feather quill',[a,c],.0017,gold)
for sign in [-1,1]:
    # Upper fan is broad at the shoulders and narrows toward the upright tip.
    for i in range(25):
        t=i/24
        a=(sign*(.16+.15*math.sin(t*math.pi)),4.38,6.73+t*.99)
        c=(sign*(.36+.25*math.sin(t*math.pi)),4.35,6.82+t*1.09)
        feather(a,c,.047)
    # Lateral fan extends horizontally with individual feathers swept toward the tips.
    for i in range(25):
        t=i/24
        a=(sign*(.15+.95*t),4.34,6.73+.13*math.sin(t*math.pi))
        c=(sign*(.30+1.04*t),4.32,6.89+.14*math.sin(t*math.pi))
        feather(a,c,.042)
    # Lower pair curves around the legs, converging below the feet.
    for i in range(27):
        t=i/26
        x=.045+.43*math.sin(t*math.pi/2);z=5.00+1.07*t
        a=(sign*x,4.36,z);c=(sign*(x+.15*math.sin(t*math.pi)),4.33,z+.17*(1-t))
        feather(a,c,.053)
    for i in range(12):
        t=i/11;feather((sign*(.13+.30*t),4.27,6.67),(sign*(.22+.35*t),4.25,6.86),.035)
# Shift hair to hug the refined head and add a darker eye line in the sculpture material.
for o in s.objects:
    if 'Long carved Christ hair' in o.name:o.location.y-=.045
    if 'Carved Christ beard' in o.name:o.location.y-=.03
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath,compress=True)
result={'file':bpy.data.filepath,'pelvis_height':pelvis_height,'vertices':len(m.vertices)}
