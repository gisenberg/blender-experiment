import bpy,math,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from scene_helpers import SceneBuilder
s=bpy.context.scene;cam=s.camera;cam.location.z=8;cam.rotation_euler=(Vector((0,6,1))-cam.location).to_track_quat('-Z','Y').to_euler()
for o in bpy.data.collections['R1 | Skip and rubble'].objects:o.location.x+=2.4;o.location.y+=3
for o in bpy.data.collections['R1 | Yard clutter'].objects:
    if o.location.x>5 and o.location.y<3 and ('drum' in o.name.lower() or 'box' in o.name.lower()):o.location.x+=2.4;o.location.y+=3
for o in bpy.data.collections['R1 | Fences and garage'].objects:
    if 'garage' in o.name.lower():o.location.y-=2
for o in bpy.data.collections['R1 | Surrounding apartment blocks'].objects:
    if 'tower' not in o.name.lower():o.location.z*=.85;o.scale.z*=.85
# Rebuild the trailer wheels in world coordinates, avoiding unevaluated matrix reads.
for o in list(bpy.data.collections['R1 | Vehicles'].objects):
    if 'Trailer road wheel' in o.name:o.hide_render=True;o.hide_set(True)
b=object.__new__(SceneBuilder);b.scene=s;b.prefix='R1';b.collections={};b.cache={};b.current=bpy.data.collections['R1 | Vehicles']
rubber=bpy.data.materials['R1 | Charred rubber and bin liners'];metal=bpy.data.materials['R1 | Dark structural galvanized metal'];rust=bpy.data.materials['R1 | Rust and exposed iron'];silver=bpy.data.materials['R1 | Aged pale galvanized flashing']
for x in [-.8,2.2]:
    for y in [-12.74,-10.92]:
        z=.57;r=.56
        b.cylinder('Corrected trailer tire',(x-.17,y,z),(x+.17,y,z),r,rubber,32)
        for xx in [x-.185,x+.185]:
            b.cylinder('Trailer wheel steel rim',(xx-.015,y,z),(xx+.015,y,z),r*.59,rust,24)
            b.cylinder('Trailer axle hub',(xx-.028,y,z),(xx+.028,y,z),r*.25,metal,20)
            for j in range(8):
                a=j*math.tau/8;yy=y+math.sin(a)*r*.40;zz=z+math.cos(a)*r*.40
                b.cylinder('Trailer rim lug',(xx-.032,yy,zz),(xx+.032,yy,zz),.026,silver,8)
        for j in range(28):
            a=j*math.tau/28;o=b.box('Trailer tire tread',(x,y+math.sin(a)*r,z+math.cos(a)*r),(.36,.105,.035),rubber,.004);o.rotation_euler.x=-a
sun=bpy.data.objects['R1 | Low warm sun'];sun.data.energy=4.2
fill=bpy.data.objects['R1 | Broad courtyard sky fill'];fill.data.color=(.92,.90,.82);fill.data.energy=900
n=s.world.node_tree.nodes;l=s.world.node_tree.links;bg=n['Background'];bg.inputs['Strength'].default_value=.30
sky=next(v for v in n if v.type=='TEX_SKY');visible=n.new('ShaderNodeBackground');visible.inputs['Strength'].default_value=1.7;l.new(sky.outputs[0],visible.inputs[0]);lp=n.new('ShaderNodeLightPath');mix=n.new('ShaderNodeMixShader');l.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);l.new(bg.outputs[0],mix.inputs[1]);l.new(visible.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],n['World Output'].inputs['Surface'])
mat=bpy.data.materials['R1 | Coarse cracked asphalt']
for node in mat.node_tree.nodes:
    if node.type=='VALTORGB':node.color_ramp.elements[0].color=(.076,.066,.050,1);node.color_ramp.elements[1].color=(.12,.106,.08,1)
s.view_settings.exposure=-.55
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'file':bpy.data.filepath,'objects':len(s.objects)}
