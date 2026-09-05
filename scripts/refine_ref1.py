import bpy,math,random
from mathutils import Vector
random.seed(19)
s=bpy.context.scene
cam=s.camera;cam.location.z=4.3;cam.rotation_euler=(Vector((0,6,1.0))-cam.location).to_track_quat('-Z','Y').to_euler()
def bygroup(name):return bpy.data.collections['R1 | '+name].objects
for o in bygroup('Utility buildings'):
    o.location.z*=1.1;o.scale.z*=1.1
for o in bygroup('Fences and garage'):
    if 'Garage' in o.name or 'garage' in o.name:
        o.location.z*=1.1;o.scale.z*=1.1
    if 'Rear blue fence' in o.name:o.location.y+=7
for o in s.objects:
    if o.name.startswith(('R1 | Near building wall','R1 | Near building horizontal cladding')):
        o.location.x-=3
        o.data=o.data.copy();o.data.materials.clear();o.data.materials.append(bpy.data.materials['R1 | Charred rubber and bin liners'])
    if o.name.startswith(('R1 | Flatbed','R1 | Trailer','R1 | Blue trailer')):
        o.location.x+=5.4
        if o.type=='MESH':
            o.location.y=-11.7+(o.location.y+11.7)*1.3
            if any(v in o.name for v in ['heavy underframe','wooden deck','deck plank','corrugated side']):o.scale.y*=1.3
for o in bygroup('Surrounding apartment blocks'):
    if 'Tower' not in o.name and 'tower' not in o.name:
        o.location.z*=.78;o.scale.z*=.78;o.location.y+=8
for o in bygroup('Trees and street furniture'):
    if 'foliage' in o.name:o.scale*=.68
for m in bpy.data.materials:
    if not m.name.startswith('R1 |') or not m.use_nodes:continue
    colors=None
    if 'asphalt' in m.name:colors=((.075,.071,.061),(.105,.101,.087))
    elif 'concrete' in m.name:colors=((.27,.26,.22),(.43,.42,.36))
    elif 'Faded blue' in m.name or 'blue corrugation' in m.name:colors=((.045,.10,.12),(.10,.23,.27))
    elif 'siding' in m.name:colors=((.25,.215,.15),(.43,.37,.26))
    elif 'leaves' in m.name:colors=((.065,.085,.03),(.15,.18,.065))
    if colors:
        for n in m.node_tree.nodes:
            if n.type=='VALTORGB':
                n.color_ramp.elements[0].color=(*colors[0],1);n.color_ramp.elements[1].color=(*colors[1],1)
for o in bygroup('Skip and rubble'):
    if 'Broken reinforced concrete slab' in o.name:
        o.data=o.data.copy()
        for v in o.data.vertices:
            v.co.x*=random.uniform(.88,1.11);v.co.y*=random.uniform(.8,1.14);v.co.z+=random.uniform(-.055,.055)
bpy.data.objects['R1 | Low warm sun'].data.energy=3
bpy.data.objects['R1 | Broad courtyard sky fill'].data.energy=650
sky=next(n for n in s.world.node_tree.nodes if n.type=='TEX_SKY');sky.air_density=1.2;sky.aerosol_density=4
s.view_settings.exposure=-.6
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'camera':list(cam.location),'saved':bpy.data.filepath}
