"""Reconstruct ref-2 as an editable, physically lit underground concourse."""
import bpy, math, random, os
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'outputs', 'ref-2')
os.makedirs(OUT, exist_ok=True)
random.seed(22)

# A separate scene preserves any work already open in Blender.
scene = bpy.data.scenes.new('Ref 2 - Abandoned underground concourse')
bpy.context.window.scene = scene
collections = {}
def group(name):
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    collections[name] = c
    return c
for name in ['Architecture', 'Ceramic cladding', 'Kiosks and signage', 'Services', 'Barriers and pallets', 'Litter', 'Lighting']:
    group(name)
current = collections['Architecture']
def move(obj, name, mat=None):
    obj.name = name
    for c in list(obj.users_collection): c.objects.unlink(obj)
    current.objects.link(obj)
    if mat: obj.data.materials.append(mat)
    return obj
def box(name, loc, size, mat, bevel=0):
    # Batch mesh creation avoids thousands of UI dependency-graph updates.
    corners=[(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata([(a*size[0]/2,b*size[1]/2,c*size[2]/2) for a,b,c in corners],[],[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)])
    o=bpy.data.objects.new(name,mesh);current.objects.link(o);o.location=loc
    if mat:mesh.materials.append(mat)
    if bevel:
        m=o.modifiers.new('Soft worn edges','BEVEL'); m.width=bevel; m.segments=2
        m=o.modifiers.new('Weighted face normals','WEIGHTED_NORMAL')
    return o
def tube(name, points, radius, mat):
    c=bpy.data.curves.new(name,'CURVE'); c.dimensions='3D'; c.resolution_u=12
    c.bevel_depth=radius; c.bevel_resolution=3
    s=c.splines.new('POLY'); s.points.add(len(points)-1)
    for p,co in zip(s.points,points): p.co=(*co,1)
    o=bpy.data.objects.new(name,c); current.objects.link(o); c.materials.append(mat)
    return o
def cylinder(name,a,b,r,mat,vertices=16):
    d=Vector(b)-Vector(a)
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=d.length, location=(Vector(a)+Vector(b))/2)
    o=move(bpy.context.object,name,mat); o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    for p in o.data.polygons: p.use_smooth=True
    return o
def material(name, color, rough=.75, metal=0, scale=5, bump=.04):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    n=m.node_tree.nodes; l=m.node_tree.links; p=n.get('Principled BSDF')
    p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metal
    tex=n.new('ShaderNodeTexNoise'); tex.noise_dimensions='3D'; tex.inputs['Scale'].default_value=scale
    tex.inputs['Detail'].default_value=5; tex.inputs['Roughness'].default_value=.72
    co=n.new('ShaderNodeTexCoord'); l.new(co.outputs['Object'],tex.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=.22
    ramp.color_ramp.elements[0].color=(*(v*.36 for v in color),1)
    ramp.color_ramp.elements[1].position=.8; ramp.color_ramp.elements[1].color=(*(min(v*1.5,1) for v in color),1)
    l.new(tex.outputs['Fac'],ramp.inputs[0]); l.new(ramp.outputs[0],p.inputs['Base Color'])
    fine=n.new('ShaderNodeTexNoise'); fine.inputs['Scale'].default_value=95; fine.inputs['Detail'].default_value=3
    l.new(co.outputs['Object'],fine.inputs['Vector'])
    b=n.new('ShaderNodeBump'); b.inputs['Strength'].default_value=.55; b.inputs['Distance'].default_value=bump
    l.new(fine.outputs['Fac'],b.inputs['Height']); l.new(b.outputs[0],p.inputs['Normal'])
    return m
def emission(name,color,power):
    m=bpy.data.materials.new(name); m.use_nodes=True; p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1); p.inputs['Emission Color'].default_value=(*color,1); p.inputs['Emission Strength'].default_value=power
    return m
concrete=material('Aged warm concrete - coarse pores',(.24,.22,.185),scale=2,bump=.025)
floor=material('Dusty stone paving',(.19,.16,.125),rough=.87,scale=3,bump=.012)
grout=material('Soot in tile joints',(.065,.051,.039),bump=.01)
tiles=[material('Oxblood glazed ceramic %02d'%i,(.115+i*.004,.049+i*.0018,.034+i*.0014),rough=.36,scale=5,bump=.004) for i in range(7)]
metal=material('Oxidized galvanized steel',(.24,.22,.18),rough=.48,metal=.7,bump=.009)
rust=material('Dark iron and rust',(.073,.044,.025),rough=.8,metal=.5,bump=.012)
shutter=material('Dust coated roller shutters',(.24,.235,.21),rough=.7,metal=.45,bump=.006)
wood=material('Splintered pallet timber',(.13,.078,.037),rough=.9,scale=3,bump=.024)
black=material('Black plastic and tar',(.009,.008,.007),rough=.48,bump=.025)
paper=material('Dirty paper scraps',(.41,.35,.23),rough=.95,bump=.005)
card=material('Flattened corrugated cardboard',(.19,.105,.052),rough=1,bump=.015)
ivory=material('Yellowed enamel trim',(.46,.44,.35),rough=.5,metal=.25,bump=.003)
red=emission('Failing red LED lettering',(.34,.013,.004),.6)

# Broad slab floor with individual joints and subtly varied worn stones.
box('Foundation',(0,5,-.16),(27,35,.3),grout)
for ix in range(-10,10):
    for iy in range(-7,20):
        box('Stone floor slab', (ix*1.35,iy*1.35,-.023-random.random()*.003),(1.342,1.342,.045),floor,.006)
box('Low concrete ceiling',(0,5,3.45),(25,34,.25),concrete)
for y in [-5,-2,1,4,7,10,13,16,19]:
    box('Transverse ceiling rib',(0,y,3.17),(25,.36,.42),concrete,.025)
for x in [-8,-4,0,4,8]:
    box('Longitudinal ceiling beam',(x,5,3.17),(.33,32,.4),concrete,.02)
box('Left perimeter wall',(-8.7,6,1.55),(.3,29,3.2),concrete)
box('Rear wall',(0,19,1.6),(25,.3,3.2),concrete)
box('Right perimeter wall',(10,6,1.6),(.25,28,3.2),concrete)

def pillar(name,x,y,w=1.55,d=1.5):
    global current
    current=collections['Architecture']; box(name+' structural core',(x,y,1.63),(w,d,3.26),grout,.008)
    current=collections['Ceramic cladding']
    cols=3; rows=7
    for iz in range(rows):
        z=(iz+.5)*3.26/rows
        for i in range(cols):
            for side in [-1,1]:
                box(name+' front/back tile',(x-w/2+(i+.5)*w/cols,y+side*(d/2+.007),z),(w/cols-.009,.025,3.26/rows-.008),random.choice(tiles),.004)
                box(name+' side tile',(x+side*(w/2+.007),y-d/2+(i+.5)*d/cols,z),(.025,d/cols-.009,3.26/rows-.008),random.choice(tiles),.004)
    current=collections['Architecture']
pillar('Hero tiled pillar',0,0)
for x,y in [(5,3.4),(7.4,7),(-5.7,8.7),(0,10),(5,12),(-5.7,15)]: pillar('Secondary support',x,y,1.2,1.15)

# Closed central kiosk, with a corridor continuing along its left side.
current=collections['Kiosks and signage']
box('Kiosk enclosed volume',(-3.9,4.4,1.5),(4.3,5.3,3),grout)
for x in [-5.9,-4.8,-3.7,-2.6,-1.8]:
    box('Kiosk brown stone plinth',(x,1.70,.31),(1.05,.16,.62),random.choice(tiles),.015)
    box('Shopfront upright',(x,1.64,1.65),(.055,.1,2.17),ivory,.006)
box('Kiosk fascia',(-3.9,1.63,2.85),(4.48,.23,.38),rust,.02)
box('Upper wall crown',(-3.9,1.85,3.1),(4.55,.5,.17),concrete,.02)
for x in [-5.36,-4.26,-3.16,-2.06]:
    box('Opaque shop window',(x,1.68,1.68),(1.03,.04,2.05),wood)
for y in [2.3,3.5,4.7,5.9,6.8]:
    box('Side kiosk window',(-6.07,y,1.67),(.04,1.07,2.03),shutter)
    box('Side mullion',(-6.1,y-.55,1.7),(.1,.06,2.5),rust)
    for z in [i*.085+.67 for i in range(24)]: box('Side shutter slat',(-6.095,y,z),(.05,1.05,.024),metal,.003)
# Poster images are original typeset reconstructions made by make_ref2_posters.py.
def poster(name,path,x,y,z,w,h):
    box(name+' backing',(x,y+.025,z),(w+.10,.09,h+.1),rust,.012)
    for xx in [x-w/2-.02,x+w/2+.02]: box(name+' vertical trim',(xx,y-.025,z),(.045,.05,h+.1),ivory,.005)
    for zz in [z-h/2-.023,z+h/2+.023]: box(name+' horizontal trim',(x,y-.025,zz),(w+.09,.05,.046),ivory,.005)
    mesh=bpy.data.meshes.new(name); mesh.from_pydata([(x-w/2,y-.035,z-h/2),(x+w/2,y-.035,z-h/2),(x+w/2,y-.035,z+h/2),(x-w/2,y-.035,z+h/2)],[],[(0,1,2,3)])
    mesh.uv_layers.new()
    for loop,uv in zip(mesh.uv_layers.active.data,[(0,0),(1,0),(1,1),(0,1)]): loop.uv=uv
    o=bpy.data.objects.new(name,mesh); current.objects.link(o)
    m=bpy.data.materials.new(name+' printed paper');m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.72
    t=m.node_tree.nodes.new('ShaderNodeTexImage'); t.image=bpy.data.images.load(path,check_existing=True);t.image.pack()
    m.node_tree.links.new(t.outputs['Color'],p.inputs['Base Color']);m.node_tree.links.new(t.outputs['Color'],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=.12
    o.data.materials.append(m)
poster('Green pharmacy advertisement',os.path.join(OUT,'pharmacy.png'),-3.28,1.49,1.73,.97,1.53)
poster('Old event poster',os.path.join(OUT,'events.png'),-4.45,1.50,1.69,.88,1.65)
poster('Graffiti on boarded window',os.path.join(OUT,'graffiti.png'),-2.08,1.52,1.62,.91,1.8)
def text_obj(name,text,loc,size,mat):
    c=bpy.data.curves.new(name,'FONT');c.body=text;c.size=size;c.extrude=.0005
    fontpath='C:/Windows/Fonts/arialbd.ttf'
    if os.path.exists(fontpath): c.font=bpy.data.fonts.load(fontpath,check_existing=True)
    o=bpy.data.objects.new(name,c);current.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0);c.materials.append(mat)
    return o
text_obj('Pharmacy sign','АПТЕКА',(-4.85,1.48,2.68),.33,ivory)
box('Dead electronic ticker',(-3.75,1.40,3.02),(3.2,.13,.26),black,.008)
text_obj('Ticker red text','ОБМЕН ВАЛЮТ   •   24 ЧАСА',(-5.2,1.32,2.97),.13,red)

# Far right shuttered shops behind the crowd-control barrier.
for x in [2.2,4.3,6.4]:
    box('Rear shop recess',(x,5.6,1.4),(2,.25,2.8),rust)
    for i in range(35): box('Roller shutter corrugation',(x,5.43,.2+i*.068),(1.86,.055,.051),shutter,.009)
    box('Shop sign',(x,5.35,2.77),(2,.12,.29),wood,.005)
    text_obj('Faded shop lettering','НА-СВЯЗИ' if x==4.3 else 'ПРЕССА',(x-.87,5.27,2.69),.20,ivory)
poster('Rear faded notices',os.path.join(OUT,'events.png'),1.45,5.20,1.72,.85,1.55)

# Left-hand passage, stairway and stainless handrails.
current=collections['Architecture']
for i in range(15):
    box('Exit stair %02d'%i,(-7.1,12.1+i*.31,.075+i*.15),(2.7,.32,.15),concrete,.012)
    box('Stair nosing',(-7.1,11.96+i*.31,.145+i*.15),(2.7,.035,.018),metal,.002)
box('Stair left cheek',(-8.55,14,1.2),(.16,4.8,2.5),concrete)
box('Stair right cheek',(-5.65,14,1.2),(.16,4.8,2.5),concrete)
for x in [-8.25,-5.93]:
    tube('Exit handrail',[(x,11.7,.85),(x,12.1,.88),(x,16.4,2.96)],.035,metal)
    for y,z in [(12.2,.92),(13.8,1.7),(15.5,2.51)]: cylinder('Handrail post',(x,y,z-.85),(x,y,z),.025,metal)

# Overhead cable bundles, conduits, junction boxes and brackets.
current=collections['Services']
for x in [-.9,-1.02,-1.14]:
    tube('Long ceiling conduit',[(x,-7,3.0),(x,0,3.0),(x,1.4,3.0),(x-.15,1.6,2.85),(x-.15,10,2.85)],.027,rust)
for y in [-1,2.4,6.4,10]:
    for z in [2.98,3.055]: tube('Cross ceiling pipe',[(-8.4,y,z),(5,y,z),(5.25,y,2.88),(5.3,y,2.52)],.025,metal)
    for x in [-6,-1,5]:
        box('Pipe hanger',(x,y,3.13),(.04,.15,.25),rust,.003)
for x,y in [(-1.05,-.1),(-6.1,1.6),(5.3,2.4)]: box('Electrical junction box',(x,y,2.88),(.19,.14,.21),metal,.02)
for x,y in [(-1,-.22),(-5.95,1.48),(4.9,3)]:
    cylinder('Camera wall bracket',(x,y,2.86),(x+.26,y-.16,2.86),.025,rust)
    o=box('Old CCTV housing',(x+.28,y-.2,2.88),(.16,.29,.13),ivory,.025);o.rotation_euler[2]=-.5
    cylinder('CCTV black lens',(x+.28,y-.34,2.88),(x+.28,y-.355,2.88),.048,black)

# Two leaning, battered steel crowd barriers, built with rounded tube corners.
current=collections['Barriers and pallets']
def barrier(x,y,width,angle=0):
    before=set(current.objects)
    r=.13; h=1.65
    pts=[(x,y,.12),(x,y,h-r)]
    for i in range(9):
        a=math.pi-i*math.pi/16;pts.append((x+r+math.cos(a)*r,y,h-r+math.sin(a)*r))
    pts.append((x+width-r,y,h))
    for i in range(9):
        a=math.pi/2-i*math.pi/16;pts.append((x+width-r+math.cos(a)*r,y,h-r+math.sin(a)*r))
    pts.append((x+width,y,.12));tube('Barrier rounded outer frame',pts,.027,metal)
    cylinder('Barrier lower rail',(x,y,.24),(x+width,y,.24),.024,metal)
    for i in range(1,int(width/.16)):
        xx=x+i*.16;cylinder('Barrier vertical rod',(xx,y,.24),(xx,y,1.61),.013,metal)
    for xx in [x+.24,x+width-.24]:
        tube('Barrier splayed foot',[(xx,y-.39,.035),(xx,y-.34,.10),(xx,y-.19,.16),(xx,y+.2,.16),(xx,y+.37,.04)],.031,rust)
        cylinder('Barrier foot stem',(xx,y,.07),(xx,y,.26),.026,metal)
    if angle:
        from mathutils import Matrix
        mat=Matrix.Translation((x,y,0))@Matrix.Rotation(angle,4,'Z')@Matrix.Translation((-x,-y,0))
        for o in set(current.objects)-before:o.matrix_world=mat@o.matrix_world
barrier(1.0,.95,2.2,-.08)
barrier(3.05,1.0,1.55,.3)
def pallet(name,loc,rot=(0,0,0)):
    parent=bpy.data.objects.new(name,None);current.objects.link(parent);parent.location=loc;parent.rotation_euler=rot
    def part(n,p,s):
        o=box(n,(0,0,0),s,wood,.014);o.parent=parent;o.location=p
    for z in [-.42,0,.42]: part('Pallet stringer',(0,.065,z),(1.13,.12,.12))
    for x in [-.49,-.25,0,.25,.49]: part('Pallet weathered slat',(x,-.04,0),(.17,.09,1.22))
    for x in [-.48,0,.48]:part('Pallet rear brace',(x,.16,0),(.13,.08,1.2))
    return parent
pallet('Leaning foreground wooden pallet',(4.55,1.95,.72),(0,-.16,-.15))
for i in range(4):pallet('Stacked shipping pallet',(7.1,5,.13+i*.17),(math.pi/2,0,.04*(i%2)))

# Refuse sacks, an abandoned wire basket, rubble and folded paper.
current=collections['Litter']
for x,y,s in [(3.45,2.0,.43),(3.9,2.35,.37),(3.25,2.55,.32),(-5.95,1.17,.22),(-6.45,1,.24)]:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3,radius=1,location=(x,y,s*.65))
    o=move(bpy.context.object,'Crumpled refuse sack',black);o.scale=(s,s*.75,s*.75)
    for v in o.data.vertices:v.co*=random.uniform(.91,1.09)
    for p in o.data.polygons:p.use_smooth=True
    cylinder('Tied rubbish bag neck',(x,y,s*1.2),(x+.025,y,s*1.48),s*.12,black)
for x in [-5.7,-5.15]:
    for y in [.75,1.23]: cylinder('Abandoned basket corner',(x,y,.08),(x,y,.54),.017,rust)
for z in [.13,.23,.33,.43,.54]:tube('Basket horizontal wire',[(-5.7,.75,z),(-5.15,.75,z),(-5.15,1.23,z),(-5.7,1.23,z),(-5.7,.75,z)],.009,rust)
for x in [-5.6,-5.5,-5.4,-5.3,-5.2]:
    tube('Basket mesh',[(x,.75,.54),(x,.75,.13),(x,1.23,.13),(x,1.23,.54)],.006,rust)
for i in range(100):
    x=random.uniform(-8,8); y=random.uniform(-2,12)
    if abs(x)<1 and abs(y)<1:continue
    if -6<x<-1.7 and 1.7<y<7:continue
    s=random.uniform(.025,.1)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=s,location=(x,y,s*.27))
    o=move(bpy.context.object,'Loose plaster rubble',concrete if i%3 else black);o.scale=(1,random.uniform(.5,1.5),.35)
for i in range(42):
    x=random.uniform(-7,6);y=random.uniform(-1,7)
    if -6<x<-1.6 and 1.7<y<7:continue
    w=random.uniform(.07,.30);h=random.uniform(.1,.36)
    mesh=bpy.data.meshes.new('Bent paper');mesh.from_pydata([(-w,-h,0),(w,-h,.014),(w,h,0),(-w,h,.02),(0,0,.03)],[],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)])
    o=bpy.data.objects.new('Loose paper and cardboard',mesh);current.objects.link(o);o.location=(x,y,.015);o.rotation_euler[2]=random.random()*6.28;mesh.materials.append(paper if i%3 else card)
for i in range(13):
    o=box('Discarded cardboard sheet',(random.uniform(1.3,4.9),random.uniform(-.7,1.6),.025+i*.001),(random.uniform(.35,.85),random.uniform(.35,.7),.008),card,.002);o.rotation_euler[2]=random.uniform(-1,1)
for x,y in [(5.7,-.2),(-6,4),(2.25,.35)]:
    cylinder('Discarded bottle',(x,y,.07),(x+.23,y+.06,.07),.045,black)
    cylinder('Bottle neck',(x+.23,y+.06,.07),(x+.30,y+.08,.07),.022,black)

current=collections['Lighting']
def light(name,loc,color,power,size,target=None,kind='AREA'):
    d=bpy.data.lights.new(name,kind);d.energy=power;d.color=color
    if kind=='AREA':d.shape='DISK';d.size=size
    else:d.shadow_soft_size=size
    o=bpy.data.objects.new(name,d);current.objects.link(o);o.location=loc
    if target:o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o
warm=emission('Warm old fluorescent',(.85,.73,.51),4)
for x,y,power in [(-3.3,1.0,95),(-6.9,5.2,65),(-7,10.3,85),(3.3,4.7,55),(7.2,9,45)]:
    box('Ceiling fluorescent fixture',(x,y,3.04),(1.05,.17,.09),rust,.015)
    box('Fluorescent diffuser',(x,y,2.988),(.92,.115,.018),warm,.012)
    light('Weak overhead fluorescent',(x,y,2.91),(1,.81,.58),power,1.1,(x,y,0))
light('Poster spill',(-3.5,.55,2.55),(1,.85,.65),38,.85,(-3.3,1.5,1.45))
light('Distant stairwell daylight',(-7.1,16,3.05),(.64,.72,.79),270,2,(-7,10,1))
light('Subtle camera-side reflected light',(1,-4.5,2.65),(.65,.56,.45),28,4,(0,0,1))
glow=emission('Dropped luminous yellow glowstick',(.66,.93,.10),9)
cylinder('Dropped glowstick',(.40,-1.08,.04),(.44,-.82,.045),.022,glow)
cylinder('Glowstick end cap',(.396,-1.10,.04),(.40,-1.065,.04),.025,ivory)
light('Glowstick local spill',(.42,-.96,.085),(.78,.68,.14),.7,.08,kind='POINT')
light('Warm reflected foreground pool',(.1,-1.4,.20),(1,.20,.06),3,.6,kind='POINT')

# Camera and a restrained cinematic finish.
d=bpy.data.cameras.new('Reference matching wide camera');cam=bpy.data.objects.new('Reference matching wide camera',d);scene.collection.objects.link(cam)
cam.location=(3.3,-6.4,1.72);target=Vector((-2.15,4,1.64));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=23;d.sensor_width=36
scene.camera=cam
scene.world=bpy.data.worlds.new('Dark underground ambient');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.15,.13,.10,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.045
scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=True
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
    for device in prefs.devices:device.use=device.type=='OPTIX'
    scene.cycles.device='GPU'
except Exception:pass
scene.cycles.max_bounces=8
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=50
scene.render.image_settings.file_format='PNG';scene.render.filepath=os.path.join(OUT,'preview.png')
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.4
scene.render.film_transparent=False
scene['reference']='ref-2.jpg'
scene['description']='Editable reconstruction: abandoned subterranean retail concourse, tiled columns, closed kiosks, barriers and litter.'
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'ref-2-reconstruction.blend'))
result={'scene':scene.name,'objects':len(scene.objects),'file':bpy.data.filepath}
