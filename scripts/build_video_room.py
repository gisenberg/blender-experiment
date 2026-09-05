"""Editable reconstruction of the visible music corner in 8c6tw_JbGRg.
Dimensions and unseen boundaries are inferred, not surveyed.
"""
import bpy, math, random, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from scene_helpers import SceneBuilder
random.seed(71)
b=SceneBuilder('Video reference - Green music room','Music room');s=b.scene
out=ROOT/'outputs'/'video-room';out.mkdir(parents=True,exist_ok=True)
def mat(name,color,rough=.5,metal=0):
    m=bpy.data.materials.new('Music room | '+name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    return m
def glow(name,color,strength):
    m=mat(name,color);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=strength;return m
def oval(name,loc,size,m):
    x,y,z=loc;o=b.cylinder(name,(x,y,z-size[2]/2),(x,y,z+size[2]/2),1,m,64);o.scale=(size[0]/2,size[1]/2,1);return o
def sphere(name,loc,scale,m):
    o=b.rock(name,loc,scale,m,0,True);sub=o.modifiers.new('Soft surface','SUBSURF');sub.levels=2;return o
def label(name,text,loc,size,m,rotation=(math.pi/2,0,0)):
    c=bpy.data.curves.new(name,'FONT');c.body=text;c.size=size;c.extrude=.0001;c.materials.append(m)
    o=bpy.data.objects.new('Music room | '+name,c);b.current.objects.link(o);o.location=loc;o.rotation_euler=rotation;return o
wall=mat('Pale sage painted plaster',(.46,.52,.46),.9)
white=mat('Warm white window frames',(.72,.74,.7),.36)
black=mat('Soft black ABS',(.009,.011,.012),.45)
rubber=mat('Rubber feet',(.007,.008,.01),.85)
chrome=mat('Polished chrome',(.58,.62,.64),.16,.96)
steel=mat('Dark mic stand steel',(.018,.022,.025),.3,.6)
ivory=mat('Ivory keyboard keys',(.82,.83,.78),.24)
navy=b.material('Deep navy woven sofa',(.026,.037,.064),.96,scale=40,bump=.001)
wood=b.material('Honey oak floor',(.29,.14,.058),.46,scale=3,bump=.0003,stretch=(1,35,3))
maple=b.material('Classical guitar spruce',(.53,.235,.066),.3,scale=3,bump=.0001,stretch=(20,3,1))
rosewood=b.material('Rosewood fretboard',(.055,.024,.014),.38,scale=8,bump=.0001,stretch=(30,3,1))
glass=mat('Clear green edge desk glass',(.73,.88,.81),.035)
p=glass.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.47
green=glow('Green LED strip',(.1,1,.4),4)
pad=glow('Mint keyboard pad border',(.18,1,.49),2)
red=glow('Red numeric LCD',(.8,.025,.008),2)
blue=glow('Blue speaker status',(.15,.35,1),2)

b.group('Architecture - observed rear wall and inferred boundaries')
b.box('Rear pale wall',(0,2.04,1.4),(4.5,.12,2.8),wall)
b.box('Inferred left wall',(-2.25,-.65,1.4),(.12,5.4,2.8),wall)
b.box('Right wall below window',(2.25,-.65,.36),(.12,5.4,.72),wall)
b.box('Right rear window pier',(2.25,1.65,1.65),(.12,.8,2.1),white)
b.box('Right front window pier',(2.25,-2.55,1.65),(.12,1.6,2.1),wall)
b.box('Right window lintel',(2.25,-.55,2.67),(.12,2.55,.27),white)
for x in range(12):
    for y in range(7):
        b.box('Oak floor board',(-2.05+x*.37,-3.15+y*.81+(x%2)*.12,-.025),(.365,.805,.05),wood,.002)
for x in [-2.16,2.16]:b.box('White skirting',(x,-.65,.07),(.035,5.35,.13),white,.007)
b.box('Rear skirting',(0,1.965,.07),(4.4,.035,.13),white,.007)
for y in [-1.75,-.7,.38,1.25]:b.box('Window vertical mullion',(2.18,y,1.67),(.095,.07,1.87),white,.012)
for z in [.74,2.57]:b.box('Window frame rail',(2.18,-.25,z),(.13,3.05,.09),white,.008)
for y in [-1.225,-.16,.81]:b.box('Night window reflective glazing',(2.22,y,1.67),(.018,1.0,1.76),glass)
b.box('Deep night outside',(3.5,-.25,1.7),(.05,4,3),mat('Night',(.001,.002,.004),1))
b.box('Broad white sill',(2.07,-.25,.73),(.38,3.15,.06),white,.01)
b.pipe('Exposed white heating pipe',[(2.07,1.73,.12),(2.07,1.73,2.72)],.017,white)
b.pipe('Heating pipe floor return',[(2.07,1.73,.12),(2.07,-1.8,.12)],.018,white)

b.group('Dark blue sofa')
for x in [-1.91,-.28]:
    for y in [1.08,1.77]:b.cylinder('Chrome sofa foot',(x,y,.03),(x,y,.16),.035,chrome,24)
b.box('Sofa upholstered base',(-1.1,1.43,.28),(2.0,.88,.34),navy,.09)
b.box('Sofa back cushion',(-1.1,1.81,.78),(2.0,.20,.75),navy,.095)
for x in [-1.59,-.62]:
    b.box('Sofa seat cushion',(x,1.33,.49),(.94,.73,.16),navy,.065)
for x in [-2.05,-.15]:b.box('Soft sofa arm',(x,1.44,.60),(.15,.84,.30),navy,.07)
seam=mat('Sofa seam',(.015,.024,.04),1)
for x in [-1.59,-.62]:b.pipe('Seat piping',[(x-.41,1.0,.49),(x+.41,1.0,.49),(x+.43,1.64,.49)],.002,seam)

b.group('Oval glass desk and equipment')
oval('Oval tempered glass desktop',(.92,1.49,.79),(1.93,.78,.018),glass)
oval('Sliding lower glass shelf',(.78,1.31,.64),(1.39,.49,.012),glass)
for x in [.15,1.64]:
    b.cylinder('Splayed chrome desk leg',(x-.09,1.15,.025),(x+.08,1.74,.76),.023,chrome,24)
    b.cylinder('Splayed chrome desk leg',(x+.09,1.79,.025),(x-.08,1.22,.76),.023,chrome,24)
    b.cylinder('Desk horizontal stretcher',(x-.06,1.19,.28),(x+.06,1.69,.28),.012,chrome,16)
silver=mat('Brushed aluminium laptop',(.39,.41,.42),.3,.7)
b.box('Closed silver laptop',(.65,1.42,.813),(.49,.33,.018),silver,.009)
oval('Laptop subtle medallion',(.65,1.42,.823),(.037,.026,.001),chrome)
b.box('Black desk mat',(1.3,1.49,.803),(.5,.38,.004),rubber,.008)
b.box('Audio interface',(.82,1.78,.85),(.22,.13,.085),steel,.014)
for x in [.75,.82,.89]:b.cylinder('Interface knob',(x,1.704,.85),(x,1.689,.85),.014,chrome,20)
b.box('Rear LED extrusion',(.99,1.93,.82),(1.75,.026,.027),black,.005)
b.box('Rear green LED diffuser',(.99,1.926,.838),(1.72,.014,.014),green,.004)
b.pipe('Desk cable',[(.82,1.79,.86),(1.08,1.82,.82),(1.67,1.7,.81),(1.87,1.68,.75),(1.86,1.7,.11)],.003,black)

b.group('Rubber plant')
pot=mat('Olive green ceramic pot',(.105,.16,.07),.26)
soil=mat('Potting soil',(.024,.016,.009),1)
b.cylinder('Tapered plant pot',(1.61,1.62,.806),(1.61,1.62,1.075),.105,pot,48,.155)
oval('Dark soil',(1.61,1.62,1.06),(.285,.285,.008),soil)
leafmats=[mat('Rubber leaf '+str(i),(.013+i*.005,.046+i*.009,.018+i*.003),.29) for i in range(4)]
stem=mat('Plant stems',(.10,.065,.025),.7)
for branch in range(3):
    bx=1.61+(branch-1)*.045;by=1.62+(branch-1)*.025
    b.pipe('Woody branching stem',[(1.61,1.62,1.04),(bx,by,1.4),(bx+(branch-1)*.12,by,1.92+branch*.05)],.009,stem)
    for k in range(9):
        z=1.21+k*.09;angle=k*2.38+branch*1.7;center=Vector((bx,by,z));direction=Vector((math.cos(angle),math.sin(angle),.25))
        end=center+direction*.23;b.pipe('Leaf petiole',[center,end],.003,stem)
        side=Vector((-math.sin(angle),math.cos(angle),0));verts=[]
        for t in range(9):
            u=t/8;half=.073*math.sin(math.pi*u);middle=end+direction*(u*.28)+Vector((0,0,.035*math.sin(math.pi*u)-.075*u*u))
            for w in [-1,0,1]:verts.append(tuple(middle+side*half*w+Vector((0,0,-.015*abs(w)*math.sin(math.pi*u)))))
        faces=[(i*3+j,i*3+j+1,(i+1)*3+j+1,(i+1)*3+j) for i in range(8) for j in range(2)]
        o=b.mesh('Glossy curved rubber leaf',verts,faces,leafmats[k%4]);o.modifiers.new('Leaf thickness','SOLIDIFY').thickness=.0008
        for p in o.data.polygons:p.use_smooth=True

b.group('Geometric kilim rug')
rugm=[b.material('Kilim yarn '+str(i),c,.98,scale=70,bump=.001) for i,c in enumerate([(.065,.14,.13),(.17,.28,.25),(.021,.039,.032),(.25,.20,.10),(.35,.36,.25)])]
b.box('Woven rug foundation',(.64,.56,.009),(2.12,2.46,.012),rugm[0],.004)
verts=[];faces=[];indices=[]
for row in range(22):
    for col in range(18):
        x=-.36+col*.117;y=-.60+row*.109;idx=len(verts)
        verts.extend([(x,y+.054,.016),(x+.055,y,.016),(x+.11,y+.054,.016),(x+.055,y+.108,.016)])
        faces.append(tuple(range(idx,idx+4)));indices.append(2 if (col+row)%3 else (1 if row%4 else 4))
o=b.mesh('Woven repeating kilim diamonds',verts,faces,rugm[0])
for m in rugm[1:]:o.data.materials.append(m)
for p,i in zip(o.data.polygons,indices):p.material_index=i
for y in [-.70,1.80]:
    for i in range(75):
        x=-.40+i*.027;b.pipe('Cotton rug fringe',[(x,y,.013),(x+.007,y+(-.055 if y<0 else .055),.009)],.0018,rugm[4])

b.group('Keyboard station beside window')
# Keyboard length follows Y so the player faces the glass, as in the oblique cut.
b.box('49 key controller chassis',(1.70,.30,.91),(.34,.92,.09),black,.018)
for i in range(29):
    y=-.12+i*.029;b.box('White piano key',(1.60,y,.966),(.205,.028,.025),ivory,.001)
    if i%7 in [0,1,3,4,5]:b.box('Raised black piano key',(1.668,y+.0145,.987),(.112,.013,.025),black,.001)
for i in range(2):
    for j in range(4):
        pos=(1.73+i*.046,-.08+j*.045,.963)
        b.box('Illuminated square pad',pos,(.039,.039,.009),pad,.003)
        b.box('Pad dark center',(pos[0],pos[1],.969),(.030,.030,.004),black,.002)
for i in range(8):b.cylinder('Rotary controller knob',(1.79,.14+i*.065,.965),(1.79,.14+i*.065,.984),.008,black,16)
b.box('Keyboard red LCD',(1.75,.66,.965),(.045,.045,.008),red,.002)
label('LCD digits','120',(1.735,.647,.972),.017,ivory,(0,0,math.pi/2))
for y in [-.03,.62]:
    b.cylinder('Keyboard stand diagonal',(1.38,y,.04),(1.87,y,.865),.016,steel,20)
    b.cylinder('Keyboard stand diagonal',(1.89,y,.04),(1.38,y,.865),.016,steel,20)
    b.cylinder('Keyboard stand floor foot',(1.3,y,.035),(1.98,y,.035),.021,rubber,20)
for y in [-.43,.98]:
    sphere('Small oval desktop speaker',(1.93,y,1.01),(.082,.075,.13),black)
    sphere('Speaker power LED',(1.855,y,1.03),(.003,.003,.003),blue)
monitor=b.box('Small angled computer display',(1.98,-.75,1.02),(.045,.34,.24),black,.008)
screen=glow('Soft laptop screen',(.31,.46,.54),.35)
b.box('Computer display luminous face',(1.954,-.75,1.02),(.004,.30,.20),screen)
b.pipe('Orange audio lead',[(1.75,.72,.90),(1.99,.7,.72),(1.99,.4,.15),(1.84,-.1,.028),(1.26,-.3,.027),(.9,-.16,.027)],.003,mat('Orange cable',(.42,.085,.016),.6))

b.group('Guitars and microphone')
def guitar(name,center,electric=False,tilt=0):
    before=set(b.current.objects);cx,cy,cz=center
    profile=[(0,.08),(.045,.15),(.11,.195),(.2,.20),(.28,.14),(.34,.115),(.4,.158),(.46,.15),(.51,.075)]
    contour=[(-w,z) for z,w in profile]+[(w,z) for z,w in reversed(profile)]
    verts=[(cx+x,cy+y,cz+z) for y in [-.043,.043] for x,z in contour];n=len(contour)
    body=mat(name+' lacquer',(.06,.008,.013),.22) if electric else maple
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    o=b.mesh(name+' carved body',verts,faces,body);be=o.modifiers.new('Rounded guitar binding','BEVEL');be.width=.014;be.segments=4;o.modifiers.new('Smooth normals','WEIGHTED_NORMAL')
    b.box(name+' fretboard',(cx,cy-.05,cz+.72),(.055,.018,.48),rosewood,.003)
    b.box(name+' headstock',(cx,cy-.035,cz+1.03),(.087,.04,.15),body,.012)
    if not electric:
        b.cylinder(name+' soundhole rosette',(cx,cy-.044,cz+.33),(cx,cy-.047,cz+.33),.065,rosewood,64)
        b.cylinder(name+' soundhole',(cx,cy-.048,cz+.33),(cx,cy-.05,cz+.33),.052,black,64)
    else:
        for z in [.21,.36]:b.box(name+' humbucker',(cx,cy-.05,cz+z),(.10,.02,.032),chrome,.003)
    b.box(name+' bridge',(cx,cy-.053,cz+.16),(.13,.02,.025),rosewood,.003)
    for i in range(19):
        z=cz+.53+.42*(1-2**(-i/12));b.cylinder(name+' fret',(cx-.027,cy-.063,z),(cx+.027,cy-.063,z),.0008,chrome,8)
    for i in range(6):
        x=cx-.02+i*.008;b.pipe(name+' string',[(x,cy-.067,cz+.16),(x,cy-.067,cz+1.07)],.00022,chrome)
        side=-1 if i<3 else 1;z=cz+.99+(i%3)*.033;b.cylinder(name+' tuning peg',(cx+side*.035,cy-.03,z),(cx+side*.065,cy-.03,z),.008,chrome,12)
    created=set(b.current.objects)-before
    parent=bpy.data.objects.new(name+' instrument assembly',None);b.current.objects.link(parent);parent.location=center
    for ob in created:ob.location-=Vector(center);ob.parent=parent
    parent.rotation_euler[1]=tilt
    return parent
guitar('Classical nylon string guitar',(-.76,.25,.16),False,-.17)
guitar('Dark red electric guitar',(-1.70,1.13,.52),True,-.45)
for x in [-.97,-.59]:b.cylinder('Guitar stand feet',(x,.10,.035),(-.77,.39,.48),.013,steel,16)
b.pipe('Guitar stand cradle',[(-.96,.24,.21),(-.96,.09,.21),(-.62,.09,.21),(-.62,.24,.21)],.012,rubber)
# Office chair without a person, to expose the furniture relationship.
oval('Black padded swivel seat',(.04,.23,.46),(.48,.47,.095),black)
b.box('Swivel chair back',(.04,.48,.76),(.43,.09,.49),black,.07)
b.cylinder('Chair gas lift',(.04,.23,.08),(.04,.23,.43),.025,chrome,24)
for i in range(5):
    a=i*math.tau/5;end=(.04+math.cos(a)*.30,.23+math.sin(a)*.30,.055)
    b.cylinder('Chair radial leg',(.04,.23,.13),end,.014,steel,16);sphere('Chair caster',end,(.025,.018,.025),black)
b.cylinder('Microphone stand',(-1.05,-.65,.08),(-1.05,-.65,1.04),.011,steel,20)
for i in range(3):
    a=i*math.tau/3;b.cylinder('Microphone tripod foot',(-1.05,-.65,.16),(-1.05+.34*math.cos(a),-.65+.34*math.sin(a),.025),.009,steel,16)
b.cylinder('Microphone boom',(-1.25,-.73,1.09),(-.36,.00,.78),.009,steel,20)
b.cylinder('Condenser microphone',(-.40,-.03,.78),(-.23,.04,.77),.035,black,32)
b.pipe('Mic lead', [(-.3,.03,.77),(-.6,-.1,.56),(-1.0,-.5,.18),(-1.1,-.6,.024),(-.3,-.85,.023),(.9,-.7,.024),(1.95,-.42,.10)],.003,black)

b.group('Lighting and reference cameras')
w=bpy.data.worlds.new('Music room dark ambient');s.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.19,.24,.3,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.055
for x in [.24,.68,1.13,1.57]:b.light('Green desk wall wash','AREA',(x,1.86,.86),5,(.06,1,.30),.38,(x,2.02,1.2))
b.light('Green glow below desk','AREA',(1.02,1.60,.66),4,(.06,1,.3),.8,(1.02,1.70,0))
b.light('Soft filming light','AREA',(-.25,-1.8,2.0),65,(.72,.82,1),2.4,(.1,1.2,.8))
b.light('Dim window ambient','AREA',(2.08,-.5,1.9),6,(.42,.58,.71),1.8,(0,.7,.8))
def camera(name,loc,target,lens):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);b.current.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens;return o
s.camera=camera('Music room - reconstructed wide view',(-.50,-3.0,1.72),(.25,.87,.94),32)
camera('Music room - frontal source angle',(-.38,-2.35,1.35),(.05,1.30,.92),40)
camera('Music room - keyboard source angle',(.13,-1.70,1.93),(1.48,.77,.98),40)
s.render.engine='CYCLES';s.cycles.samples=128;s.cycles.use_denoising=True;s.cycles.max_bounces=10;s.cycles.transmission_bounces=8
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
s.cycles.device='GPU';s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
s.render.filepath=str(out/'music-room-still.png');s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0
s['reference_url']='https://www.youtube.com/watch?v=8c6tw_JbGRg'
s['reconstruction_scope']='Visible music corner inferred from frontal guitar and oblique keyboard views. Room dimensions, unseen boundaries, and instrument resting positions are approximate. No measured survey or full photogrammetry.'
s['assumed_room_width_m']=4.4;s['assumed_ceiling_height_m']=2.8
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'music-room-reconstruction.blend'))
result={'file':bpy.data.filepath,'scene':s.name,'objects':len(s.objects)}
