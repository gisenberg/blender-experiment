import bpy, math
from mathutils import Vector
scene=bpy.data.scenes['Ref 2 - Abandoned underground concourse'];bpy.context.window.scene=scene
cam=scene.camera;cam.location.z=1.4;cam.rotation_euler=(Vector((-2.15,4,.3))-cam.location).to_track_quat('-Z','Y').to_euler()
for o in bpy.data.collections['Kiosks and signage'].objects:
    if o.name.startswith(('Green pharmacy advertisement','Old event poster')):o.location.z-=.16
for name,power in [('Distant stairwell daylight',95),('Stairwell broad fill',30),('Warm reflected foreground pool',8)]:bpy.data.objects[name].data.energy=power
for o in bpy.data.collections['Lighting'].objects:
    if o.name.startswith('Left corridor pool'):o.data.energy=28;o.data.color=(.83,.79,.66)
scene.view_settings.exposure=-.45
for m in bpy.data.materials:
    if m.use_nodes and m.name.startswith(('Oxblood','Dusty stone','Aged warm concrete','Splintered')):
        n=m.node_tree.nodes;l=m.node_tree.links;g=n.new('ShaderNodeNewGeometry')
        for t in n:
            if t.type=='TEX_NOISE':l.new(g.outputs['Position'],t.inputs['Vector'])
scene.render.resolution_percentage=100;scene.cycles.samples=256
scene.render.filepath=bpy.path.abspath('//ref-2-render.png')
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'saved':bpy.data.filepath}
