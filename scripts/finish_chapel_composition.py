"""Final architectural detail and camera alignment for the researched chapel."""
import bpy,math,sys
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from scene_helpers import SceneBuilder
s=bpy.context.scene;b=SceneBuilder.__new__(SceneBuilder);b.scene=s;b.prefix='REFINED';b.cache={};b.collections={};b.group('Tabernacle miniature carved friezes')
gold=bpy.data.materials['Chapel | Aged warm gold leaf'];bright=bpy.data.materials['Chapel | Polished raised gilding'];panel=bpy.data.collections['Chapel | Carved panel master']
for o in s.objects:
    if 'Long straight gold glory ray' in o.name or 'Dark vertical cross behind vision' in o.name:o.hide_render=False;o.hide_viewport=False
for j in range(6):
    w=2.48-j*.30;y=4.40+j*.05;z=1.47+j*.28
    o=bpy.data.objects.new('REFINED | Tier carved frieze',None);o.instance_type='COLLECTION';o.instance_collection=panel;b.current.objects.link(o);o.location=(0,y-.397,z);o.scale=(w/1.5,.10,.09)
    for sign in [-1,1]:
        pts=[]
        for k in range(45):
            t=k/44;a=t*math.tau*1.2;r=.095*(1-.9*t);pts.append((sign*w/2+sign*r*math.cos(a),y-.45,z+r*math.sin(a)))
        b.pipe('Gilt tabernacle corner volute',pts,.013,bright)
b.group('Altar central cartouche')
for r,width in [(1,.021),(.86,.012)]:
    b.pipe('Altar oval cartouche border',[(.36*r*math.cos(i*math.tau/90),2.99,1.04+.29*r*math.sin(i*math.tau/90)) for i in range(91)],width,gold)
for k in range(12):
    a=k*math.tau/12
    b.pipe('Altar cartouche curled spray',[(.10*math.cos(a),2.98,1.04+.10*math.sin(a)),(.23*math.cos(a+.15),2.97,1.04+.20*math.sin(a+.15)),(.28*math.cos(a+.32),2.97,1.04+.23*math.sin(a+.32))],.016,bright)
# Distinguish the right-hand polychrome sculpture's dark blue-green garment.
m=bpy.data.materials.new('REFINED | Dark blue-green statue garment');m.diffuse_color=(.018,.043,.045,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.018,.043,.045,1);p.inputs['Roughness'].default_value=.8
o=next(o for o in s.objects if 'Right foreground Franciscan' in o.name);o.data=o.data.copy();o.data.materials[0]=m
s.camera.location=(0,-5.65,1.69);s.camera.rotation_euler=(Vector((0,4.46,3.36))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.lens=28
s.camera.name='São Francisco - revised frame 8 camera'
def camera(name,loc,target,lens):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);b.current.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens;return o
camera('São Francisco - scanned statue detail',(-1.3,-3.20,1.80),(-2.35,-.20,1.58),48)
camera('São Francisco - carving panel detail',(-.50,-1.9,3.22),(-2.98,-.9,3.52),58)
s['camera_alignment_notes']='Adjusted vertical framing using the altar top and foreground statue heights in the eight-second source. Dimensions remain inferred; this is not a surveyed camera solve.'
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath,compress=True)
result={'file':bpy.data.filepath,'cameras':3}
