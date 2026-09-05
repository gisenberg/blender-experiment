import bpy, math, random, os
from mathutils import Vector, Matrix
scene=bpy.data.scenes['Ref 2 - Abandoned underground concourse'];bpy.context.window.scene=scene
random.seed(31)
def mat(name):return bpy.data.materials[name]
concrete=mat('Aged warm concrete - coarse pores');metal=mat('Oxidized galvanized steel');rust=mat('Dark iron and rust');shutter=mat('Dust coated roller shutters')
collection=bpy.data.collections['Architecture']
def box(name,loc,size,material):
    verts=[(a*size[0]/2,b*size[1]/2,c*size[2]/2) for a,b,c in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)])
    o=bpy.data.objects.new(name,mesh);collection.objects.link(o);o.location=loc;mesh.materials.append(material)
    return o
cam=scene.camera;cam.location.z=.87;cam.rotation_euler=(Vector((-2.15,4,.79))-cam.location).to_track_quat('-Z','Y').to_euler()
for o in scene.objects:
    if o.name.startswith('Hero tiled pillar'):
        o.location.x=o.location.x*.70+.45;o.location.y=o.location.y*.70-1.25;o.scale.x*=.70;o.scale.y*=.70
    if o.name.startswith(('Barrier ',)):
        o.location.x-=.12;o.location.y+=.65
    if o.name=='Leaning foreground wooden pallet':o.location.x-=.7;o.location.y-=.35;o.scale*=1.1
    if o.name.startswith(('Dropped glowstick','Glowstick end cap','Glowstick local spill')):o.location.y-=1.15
    if o.name=='Warm reflected foreground pool':o.location.y-=.8
    if o.name=='Left perimeter wall':o.hide_render=True;o.hide_set(True)
for o in bpy.data.collections['Kiosks and signage'].objects:
    if o.location.x < -1:o.location.x-=.60
    elif o.type=='MESH' and o.name.startswith(('Green pharmacy advertisement','Old event poster','Graffiti on boarded window')):
        o.location.x-=.60
# Relocate the stairs so the flight recedes along the left-hand corridor.
transform=Matrix.Translation((-16,4,0))@Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation((7.1,-12.1,0))
for o in scene.objects:
    if o.name.startswith(('Exit stair','Stair nosing','Stair left cheek','Stair right cheek','Exit handrail','Handrail post')):o.matrix_world=transform@o.matrix_world
for name in ['Low concrete ceiling','Foundation']:
    o=bpy.data.objects[name];o.scale.x=2;o.location.x=-6
for o in scene.objects:
    if o.name.startswith('Transverse ceiling rib'):o.scale.x=2;o.location.x=-6
box('Far left corridor back wall',(-14,6,1.65),(16,.22,3.3),concrete)
box('Far left corridor near wall',(-14,1.95,1.65),(14,.22,3.3),concrete)
for x in [-8,-10.5,-13,-15.5,-18,-20.5]:
    box('Passage overhead crossbeam',(x,4,3.08),(.3,4.4,.40),concrete)
    box('Passage shop dark recess',(x,5.84,1.43),(2.1,.08,2.55),rust)
    for i in range(32):box('Passage shop shutter',(x,5.78,.22+i*.073),(2.06,.06,.058),shutter)
    box('Passage storefront mullion',(x+1.1,5.68,1.5),(.08,.12,3),metal)
# Continued paving beneath the newly visible passage.
for x in range(-20,-9):
    for y in range(1,6):box('Passage paving',(x*1.35,y*1.35,-.027),(1.341,1.341,.045),mat('Dusty stone paving'))
collection=bpy.data.collections['Lighting']
def area(name,loc,power,color,size,target):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=color;d.shape='DISK';d.size=size
    o=bpy.data.objects.new(name,d);collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o
o=bpy.data.objects['Distant stairwell daylight'];o.location=(-19.8,4,3);o.rotation_euler=(Vector((-14.8,4,.5))-o.location).to_track_quat('-Z','Y').to_euler();o.data.energy=450
for x,p in [(-9,65),(-12,65),(-15,70)]:area('Left corridor pool of light',(x,4,2.94),p,(.83,.80,.65),1.6,(x,4,0))
area('Soft light on barrier',(2,1.5,2.65),30,(.8,.67,.5),2,(2,1.5,0))
for o in collection.objects:
    if o.name.startswith('Weak overhead fluorescent') and o.location.x>0:o.data.energy*=.48
for n in concrete.node_tree.nodes:
    if n.type=='BUMP':n.inputs['Distance'].default_value=.009
for n in mat('Dusty stone paving').node_tree.nodes:
    if n.type=='BUMP':n.inputs['Distance'].default_value=.004
scene.view_settings.exposure=-.5
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'objects':len(scene.objects),'saved':bpy.data.filepath}
