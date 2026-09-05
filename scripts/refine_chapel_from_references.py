"""Museum-photo refinement of the Sao Francisco da Penitencia reconstruction.
Run on the original chapel project. External meshes are CC0; see ASSET_SOURCES.md.
"""
import bpy, math, random, sys
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from scene_helpers import SceneBuilder
s=bpy.context.scene;s.name='São Francisco da Penitência - reference refinement'
OUT=ROOT/'outputs/polyphia-room';random.seed(110)
b=SceneBuilder.__new__(SceneBuilder);b.scene=s;b.prefix='REFINED';b.cache={};b.collections={}
b.ico=next(o.data for o in s.objects if 'Ceiling gilt boss' in o.name)
def mat(name,c,rough=.6,metal=0):
    m=bpy.data.materials.new('REFINED | '+name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
gold=bpy.data.materials['Chapel | Aged warm gold leaf'];bright=bpy.data.materials['Chapel | Polished raised gilding'];dark=bpy.data.materials['Chapel | Recessed bronze gold'];wood=bpy.data.materials['Chapel | Deep umber carving recess']
flesh=mat('Aged polychrome sculpture flesh',(.39,.23,.13),.5)
cloth=mat('Franciscan umber habit',(.047,.026,.016),.88)
hair=mat('Dark carved hair',(.023,.012,.006),.58)
cord=mat('Franciscan rope',(.42,.33,.19),.86)
wingmat=mat('Old gold feather polychrome',(.47,.36,.18),.53,.23)
clothivory=mat('Ivory carved loincloth',(.50,.39,.23),.75)
burgundy=mat('Brocade burgundy ground',(.075,.020,.012),.92)
def hide(o):o.hide_render=True;o.hide_viewport=True
def smooth(o):
    for p in o.data.polygons:p.use_smooth=True
    return o
def leaf(a,c,width,material=gold,name='Carved acanthus',depth=.024):
    a=Vector(a);c=Vector(c);d=c-a;side=Vector((d.z,0,-d.x)).normalized();verts=[];n=19
    for i in range(n):
        t=i/(n-1);mid=a+d*t;w=width*math.sin(math.pi*t)**.75*(.78+.22*math.cos(t*math.pi*10))
        for j in range(5):
            v=j/2-1;ridge=depth*math.sin(math.pi*t)*(1-.75*abs(v))
            verts.append(tuple(mid+side*w*v+Vector((0,-ridge,0))))
    return smooth(b.mesh(name,verts,[(i*5+j,i*5+j+1,(i+1)*5+j+1,(i+1)*5+j) for i in range(n-1) for j in range(4)],material))
def scroll(x,y,z,r,sign=1,vertical=1):
    verts=[];steps=70;sections=7
    for i in range(steps):
        t=i/(steps-1);a=t*math.tau*1.23;radius=r*(1-.94*t);w=r*(.105-.074*t)
        p=Vector((x+sign*radius*math.cos(a),y,z+vertical*radius*math.sin(a)));perp=Vector((sign*math.cos(a),0,vertical*math.sin(a)))
        for j in range(sections):
            q=j/(sections-1)*2-1;profile=.018*(1-q*q)*(1+.12*math.cos(q*math.pi*4))
            verts.append(tuple(p+perp*w*q+Vector((0,-profile,0))))
    return smooth(b.mesh('Fluted undercut volute',verts,[(i*sections+j,i*sections+j+1,(i+1)*sections+j+1,(i+1)*sections+j) for i in range(steps-1) for j in range(sections-1)],gold))
def instance(name,col,loc,scale=(1,1,1),rot=0):
    o=bpy.data.objects.new(name,None);o.instance_type='COLLECTION';o.instance_collection=col;b.current.objects.link(o);o.location=loc;o.scale=scale;o.rotation_euler.z=rot;return o

# Replace the repeated large generic ornament with a deeply layered carved panel.
panel=bpy.data.collections['Chapel | Carved panel master'];b.current=panel
for o in list(panel.objects):
    if not any(t in o.name for t in ['Panel shadowed backing','Gilded frame']):hide(o)
for side in [-1,1]:
    b.pipe('Rising ogee vine',[(side*(.045+.07*math.sin(i*.22)),-.17,-.94+i*.047) for i in range(41)],.016,gold)
    for row,z in enumerate([-.69,-.10,.49]):
        x=side*(.34 if row!=1 else .40);scroll(x,-.20,z,.28,side,-1 if row%2 else 1)
        for k in range(11):
            a=k*math.tau/11;px=x+.24*math.cos(a);pz=z+.24*math.sin(a)
            leaf((px,-.19,pz),(px+.15*math.cos(a),-.225,pz+.15*math.sin(a)),.057,bright,depth=.035)
        leaf((side*.07,-.19,z-.30),(side*.29,-.26,z+.28),.16,gold,depth=.07)
    for z in [-.90,-.43,.16,.79]:
        scroll(side*.54,-.19,z,.115,-side)
        leaf((side*.40,-.20,z-.14),(side*.59,-.23,z+.17),.07)
for z in [-.80,-.29,.27,.82]:
    for k in range(10):
        a=k*math.tau/10;leaf((0,-.21,z),(.13*math.cos(a),-.24,z+.13*math.sin(a)),.035,bright)

# Correct backdrop: fine gold floral damask on a red-brown ground, not rings.
for o in list(s.objects):
    if any(t in o.name for t in ['Niche brocade lozenge','Niche flower stud','Rear tall relief field']):hide(o)
    if 'Central luminous gilt niche' in o.name:o.data=o.data.copy();o.data.materials.clear();o.data.materials.append(burgundy)
b.group('Floral damask master');damask=b.current
for sign in [-1,1]:
    b.pipe('Fine brocade stem',[(sign*.012,0,-.18),(sign*.029,-.001,-.06),(sign*.013,0,.10),(0,0,.18)],.0028,bright)
    for z in [-.105,-.02,.064]:
        leaf((sign*.014,0,z),(sign*.072,0,z+.061),.021,bright,depth=.001)
        scroll(sign*.052,0,z,.034,sign)
leaf((0,0,.065),(0,0,.18),.025,bright,depth=.001)
s.collection.children.unlink(damask)
b.group('Reference-matched floral backdrop')
for row in range(15):
    for col in range(13):
        instance('Gold damask repeat',damask,(-1.11+col*.18+(row%2)*.09,5.045,2.31+row*.305),(.94,.10,.80))

# Four torsional columns, in two staggered planes, and the arched canopy.
for o in list(s.objects):
    if any(t in o.name for t in ['Carved column shadow core','Spiral gilded column vine','Column vine leaf','Column moulded collar','Corinthian capital leaf','Column square abacus']):hide(o)
    if any(c.name=='Chapel | Additional dense column foliage' for c in o.users_collection):hide(o)
b.group('Staggered Solomonic columns')
for x,y in [(-2.13,4.77),(-1.50,5.05),(1.50,5.05),(2.13,4.77)]:
    z0=1.92;h=5.10;verts=[];N=64;M=100
    for j in range(M):
        t=j/(M-1);cx=x+.045*math.sin(t*math.tau*3);cy=y+.045*math.cos(t*math.tau*3)
        for i in range(N):
            a=i*math.tau/N;r=.23*(1+.13*math.cos(a*3-t*math.tau*6));verts.append((cx+r*math.cos(a),cy+r*math.sin(a),z0+t*h))
    smooth(b.mesh('Twisted carved column shaft',verts,[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(M-1) for i in range(N)],dark))
    for j in range(48):
        t=j/47;z=z0+t*h
        for k in range(4):
            a=t*math.tau*3+k*math.tau/4;xx=x+math.cos(a)*.255;yy=y+math.sin(a)*.255
            leaf((xx,yy,z),(xx+.095*math.cos(a),yy-.02,z+.19),.080,gold,depth=.04)
    for z,r in [(1.87,.34),(1.98,.29),(7.0,.30),(7.12,.36)]:
        b.cylinder('Refined column collar',(x,y,z),(x,y,z+.075),r,gold,48)
    for k in range(10):
        a=k*math.tau/10;leaf((x+math.cos(a)*.24,y+math.sin(a)*.24,6.83),(x+math.cos(a)*.39,y+math.sin(a)*.39,7.15),.09,bright,depth=.04)
b.group('Rounded gilded altar canopy')
for offset in [0,.10,.20,.30]:
    pts=[((2.39-offset)*math.cos(i*math.pi/100),4.59-offset*.12,6.83+(1.03-offset*.22)*math.sin(i*math.pi/100)) for i in range(101)]
    b.pipe('Arched canopy moulding',pts,.055 if offset<.25 else .035,gold)
for i in range(27):
    a=.05+i*(math.pi-.1)/26;x=2.28*math.cos(a);z=6.83+.99*math.sin(a)
    scroll(x,4.49,z,.095,1 if i%2 else -1)

# Remove the old toy-like statue assemblies, halos, and sunburst.
for o in list(s.objects):
    if any(t in o.name for t in ['Central niche saint','Small tabernacle figure','Side wall saint','Gilded attendant','Central heavenly figure','Spread carved wing feather','Large descending wing feather','Long gilded sun ray','Carved statue eye','Statue brow','Carved mouth','Sculpted beard fold','Saint halo']):hide(o)

# Museum scan: normalize once, preserve sculpted folds and face, and share the mesh.
b.group('Museum-scan Franciscan statues')
source=bpy.data.objects.get('REFINED | SMK Saint Francis source scan')
if source is None:
    bpy.ops.wm.stl_import(filepath=str(ROOT/'assets/statues/francis-assisi-smk.stl'));source=bpy.context.object;source.name='REFINED | SMK Saint Francis source scan'
lo=Vector([min(v.co[i] for v in source.data.vertices) for i in range(3)]);hi=Vector([max(v.co[i] for v in source.data.vertices) for i in range(3)])
mesh=source.data.copy()
for v in mesh.vertices:v.co=(v.co-Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z)))/(hi.z-lo.z)
mesh.materials.clear()
for m in [cloth,flesh,hair,cord]:mesh.materials.append(m)
for p in mesh.polygons:
    p.use_smooth=True;c=sum((mesh.vertices[i].co for i in p.vertices),Vector())/len(p.vertices)
    p.material_index=1 if (c.z>.875 and c.y<-.02 and abs(c.x)<.105) or (.56<c.z<.76 and c.y<-.125 and abs(c.x)<.11) else 0
    if c.z>.968:p.material_index=2
hide(source)
for name,loc,height,rot in [('Saint Francis looking toward the vision',(-.36,4.40,3.07),1.38,math.radians(146)),('Left foreground Franciscan',(-2.35,-.22,.57),1.62,.15),('Right foreground Franciscan',(2.35,-.22,.57),1.62,-.24),('Left altar attendant',(-1.96,4.1,1.72),.98,0),('Right altar attendant',(1.96,4.1,1.72),.98,0)]:
    o=bpy.data.objects.new('REFINED | '+name,mesh);b.current.objects.link(o);o.location=loc;o.scale=(height,)*3;o.rotation_euler.z=rot
    mod=o.modifiers.new('Retain detailed scan with lighter triangulation','DECIMATE');mod.ratio=.38

# Anatomical mesh for the six-winged Christ, with a gently raised cruciform pose.
b.group('Cristo Serafico anatomical sculpture')
vs=[];faces=[];groups={};group=''
for line in (ROOT/'assets/statues/makehuman-base.obj').read_text().splitlines():
    if line.startswith('v '):vs.append(Vector(tuple(map(float,line.split()[1:4]))))
    elif line.startswith('g '):group=line[2:];groups.setdefault(group,[])
    elif line.startswith('f '):
        f=[int(x.split('/')[0])-1 for x in line.split()[1:]];groups.setdefault(group,[]).extend(f)
        if group=='body':faces.append(f)
used=sorted(set(i for f in faces for i in f));index={v:i for i,v in enumerate(used)}
def joint(name):
    ids=set(groups[name]);return sum((vs[i] for i in ids),Vector())/len(ids)
bottom=min(vs[i].y for i in used);top=max(vs[i].y for i in used);height=top-bottom
verts=[]
for idx in used:
    v=vs[idx].copy();sign=1 if v.x>0 else -1
    if abs(v.x)>1.18 and v.y>1.2:
        origin=joint('joint-l-shoulder' if sign>0 else 'joint-r-shoulder');weight=max(0,min(1,(abs(v.x)-1.18)/1.0));angle=math.radians(67)*sign*weight
        v=origin+Matrix.Rotation(angle,3,'Z')@(v-origin)
    if v.y<.6:v.x*=1-.77*max(0,min(1,(.6-v.y)/7.6))
    if v.y>6.0:
        origin=joint('joint-neck');weight=max(0,min(1,(v.y-6.0)/.7));v=origin+Matrix.Rotation(math.radians(12)*weight,3,'X')@Matrix.Rotation(math.radians(9)*weight,3,'Z')@(v-origin)
    verts.append((v.x/height*2.02,-v.z/height*2.02,(v.y-bottom)/height*2.02))
body=b.mesh('Cristo Serafico anatomical body',verts,[[index[i] for i in f] for f in faces],flesh,(0,4.19,5.03));smooth(body)
sub=body.modifiers.new('Sculpture surface smoothing','SUBSURF');sub.levels=1
# Loincloth with diagonal gathered folds; body remains an editable independent mesh.
verts=[];M=28;N=80
for j in range(M):
    t=j/(M-1)
    for i in range(N):
        a=i*math.tau/N;r=.145+.025*t+.014*math.sin(a*13+t*5)+.009*math.sin(a*23-t*7)
        z=5.94-.31*t+.055*math.sin(a+1.0)*(1-t)
        verts.append((math.cos(a)*r,4.18+math.sin(a)*r*.67,z))
smooth(b.mesh('Gathered ivory loincloth',verts,[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(M-1) for i in range(N)],clothivory))
for k in range(6):
    b.pipe('Carved hanging cloth fold',[(-.14-k*.007,4.06,5.95),(-.26-k*.012,4.03,5.80),(-.27+k*.006,4.04,5.59),(-.21+k*.007,4.02,5.47)],.010,clothivory)
# Individually curved hair locks and a short beard around the anatomical head.
for sign in [-1,1]:
    for k in range(10):
        x=sign*(.062+k*.006)
        b.pipe('Long carved Christ hair',[(x,4.15,6.96),(x+sign*.035,4.08,6.84),(x+sign*.043,4.07,6.70),(x+sign*.066,4.06,6.57)],.009,hair)
for k in range(9):
    x=-.036+k*.008;b.pipe('Carved Christ beard',[(x,4.00,6.78),(x*.6,4.00,6.69),(x*.3,4.03,6.65)],.006,hair)

# Six wings: upright, lateral, and downward pairs, based on the museum close-up.
b.group('Six pairs arrangement - three feathered wing pairs')
def feather(a,c,width):
    a=Vector(a);c=Vector(c);mid=a.lerp(c,.52);mid.y-=.018
    pts=[a.lerp(c,t)+Vector((0,-.035*math.sin(t*math.pi),.018*math.sin(t*math.pi))) for t in [i/24 for i in range(25)]]
    leaf(a,c,width,wingmat,'Layered carved flight feather',.025)
    b.pipe('Feather central quill',pts,.0025,bright)
for sign in [-1,1]:
    for k in range(24):
        t=k/23
        feather((sign*.10,4.39,6.75),(sign*(.30+.25*math.sin(t*2.6)),4.43,7.08+.98*t),.052)
        feather((sign*.12,4.40,6.73),(sign*(.52+.80*t),4.40,6.79+.27*math.sin(t*2.3)),.056)
        feather((sign*.06,4.34,5.03),(sign*(.24+.43*math.sin(t*1.8)),4.39,5.26+.88*t),.059)
    # Intermediate smaller coverts conceal the feather roots.
    for k in range(12):
        t=k/11;feather((sign*.09,4.30,6.68),(sign*(.18+.43*t),4.29,6.78+.22*math.sin(t*2.8)),.044)
b.box('Dark vertical cross behind vision',(0,4.49,6.13),(.115,.07,3.95),wood,.004)
for i in range(43):
    a=.03+i*math.tau/43;r0=.36;r1=1.49+random.uniform(-.17,.14);width=.012 if i%3 else .026
    x,z=math.cos(a),math.sin(a)
    b.mesh('Long straight gold glory ray',[(x*r0,4.51,6.44+z*r0),(x*r1,4.51,6.44+z*r1),(math.cos(a+width)*r0,4.51,6.44+math.sin(a+width)*r0)],[(0,1,2)],bright)

# Bowed altar: denser asymmetrical surface scrolls and small sprays.
b.group('Reference altar surface carving')
for o in list(s.objects):
    if 'Altar gilded spray' in o.name:hide(o)
for x in [-1.30,-.90,-.45,0,.45,.90,1.30]:
    scroll(x,3.04,1.10,.15,1 if x>=0 else -1)
    for sign in [-1,1]:leaf((x,3.03,.78),(x+sign*.17,3.00,1.39),.055,bright,depth=.023)

# Refine lighting and framing against the source, keeping a recoverable original camera.
s.camera.location=(0,-5.65,1.69);s.camera.rotation_euler=(Vector((0,4.46,3.60))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.lens=28
for o in s.objects:
    if o.type=='LIGHT':
        if 'Altar warm overhead' in o.name:o.data.energy=85
        if 'Soft warm frontal bounce' in o.name:o.data.energy=190;o.data.color=(1,.86,.66)
s.view_settings.exposure=-1.05;s.cycles.samples=192
s['reference_research']='Museum official gallery and virtual tour confirm Cristo Serafico with three wing pairs, four staggered Solomonic columns, rounded canopy, and floral brocade.'
s['statue_provenance']='Saint Francis: CC0 SMK scan KAS1959, a substitute sculpture rather than a scan of the Rio statue. Christ anatomy: CC0 MakeHuman base mesh with custom pose, hair, drapery, wings.'
s.render.filepath=str(OUT/'gilded-chapel-refined-still.png')
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'gilded-chapel-refined.blend'))
result={'scene':s.name,'file':bpy.data.filepath,'objects':len(s.objects)}
