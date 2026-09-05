import bpy, math, os, random
from mathutils import Vector
scene=bpy.data.scenes['Ref 2 - Abandoned underground concourse'];bpy.context.window.scene=scene
o=bpy.data.objects['Far left corridor near wall'];o.hide_render=True;o.hide_set(True)
for o in scene.objects:
    if o.name.startswith(('Dropped glowstick','Glowstick end cap','Glowstick local spill')):o.location.x+=.65
    if o.name=='Leaning foreground wooden pallet':o.rotation_euler.y+=math.pi/2
    if o.name=='Subtle camera-side reflected light':o.data.energy=10
for m in bpy.data.materials:
    if m.name.startswith('Oxblood'):m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.48
# Pale ambient bounce makes the distant passage legible without flattening the foreground.
d=bpy.data.lights.new('Stairwell broad fill','AREA');d.energy=110;d.color=(.65,.72,.78);d.shape='DISK';d.size=2
o=bpy.data.objects.new('Stairwell broad fill',d);bpy.data.collections['Lighting'].objects.link(o);o.location=(-15,3.5,2.9);o.rotation_euler=(Vector((-17,4,1.2))-o.location).to_track_quat('-Z','Y').to_euler()
# A subtle photographic glow is kept adjustable in the compositor.
g=bpy.data.node_groups.get('Reference lens finish') or bpy.data.node_groups.new('Reference lens finish','CompositorNodeTree')
g.nodes.clear()
if not len(g.interface.items_tree):g.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
rl=g.nodes.new('CompositorNodeRLayers');rl.scene=scene;rl.location=(-400,100)
gl=g.nodes.new('CompositorNodeGlare');gl.inputs['Type'].default_value='Fog Glow';gl.inputs['Threshold'].default_value=1.3;gl.inputs['Strength'].default_value=.18;gl.inputs['Size'].default_value=.35;gl.location=(-160,100)
out=g.nodes.new('NodeGroupOutput');out.location=(100,100);g.links.new(rl.outputs['Image'],gl.inputs['Image']);g.links.new(gl.outputs['Image'],out.inputs['Image']);scene.compositing_node_group=g
scene.render.resolution_percentage=50;scene.cycles.samples=64
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'saved':bpy.data.filepath}
