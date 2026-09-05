import bpy,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from scene_helpers import SceneBuilder
s=bpy.context.scene;b=object.__new__(SceneBuilder);b.scene=s;b.prefix='R1';b.collections={};b.cache={};b.current=bpy.data.collections['R1 | Fences and garage']
trim=bpy.data.materials['R1 | Dark structural galvanized metal']
for i in range(31):b.box('Garage right wall siding joint',(-3.985,-2.2,.13+i*.125),(.035,4.68,.017),trim)
for o in bpy.data.collections['R1 | Fences and garage'].objects:
    if o.type=='FONT' and 'graffiti' in o.name.lower():o.scale.x*=1.85;o.scale.y*=1.5
mat=bpy.data.materials['R1 | Coarse cracked asphalt']
for n in mat.node_tree.nodes:
    if n.type=='TEX_NOISE' and n.inputs['Scale'].default_value<5:n.inputs['Scale'].default_value=9
    if n.type=='VALTORGB':n.color_ramp.elements[0].color=(.082,.077,.065,1);n.color_ramp.elements[1].color=(.108,.10,.084,1)
deck=b.material('Dull weathered trailer deck',(.19,.24,.23),rough=.8,metal=.35,scale=7,bump=.01)
for o in bpy.data.collections['R1 | Vehicles'].objects:
    if 'deck plank' in o.name:o.data.materials.clear();o.data.materials.append(deck)
b.current=bpy.data.collections['R1 | Ground and roads']
b.pipe('Long foreground asphalt fissure',[(9,-17,-.014),(8.6,-15,-.014),(9.1,-13,-.014),(8.7,-11,-.014),(9.1,-9,-.014),(8.4,-7,-.014),(8.8,-5,-.014),(8.1,-3,-.014)],.018,bpy.data.materials['R1 | Mortar and road cracks'])
b.pipe('Branching road crack',[(8.7,-11,-.012),(7.9,-10.5,-.012),(7.4,-9.3,-.012),(6.7,-8.5,-.012)],.012,bpy.data.materials['R1 | Mortar and road cracks'])
b.current=bpy.data.collections['R1 | Lighting and camera.001'] if 'R1 | Lighting and camera.001' in bpy.data.collections else bpy.data.collections['R1 | Lighting and camera']
fog=bpy.data.materials.new('R1 | Distant urban haze');fog.use_nodes=True;n=fog.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');v=n.new('ShaderNodeVolumeScatter');v.inputs['Color'].default_value=(.83,.83,.78,1);v.inputs['Density'].default_value=.009;v.inputs['Anisotropy'].default_value=.2;fog.node_tree.links.new(v.outputs[0],out.inputs['Volume'])
o=b.box('Distant softened air',(0,40,12),(100,40,25),None);o.data=o.data.copy();o.data.materials.append(fog);o.display_type='WIRE'
b.light('Warm ambient light on distant facades','AREA',(0,18,17),6500,(1,.94,.80),35,(0,38,8))
s.render.resolution_percentage=100;s.cycles.samples=128;s.render.filepath=str(ROOT/'outputs'/'ref-1'/'ref-1-still.png')
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'file':bpy.data.filepath,'still':s.render.filepath}
