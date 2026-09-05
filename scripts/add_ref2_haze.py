"""Add shallow, smoothly varying underground dust haze to the animation."""
import bpy, os
scene=bpy.context.scene
collection=bpy.data.collections.new('Atmosphere');scene.collection.children.link(collection)
material=bpy.data.materials.new('Subtle airborne dust - background depth');material.use_nodes=True
n=material.node_tree.nodes;l=material.node_tree.links;n.clear()
out=n.new('ShaderNodeOutputMaterial');volume=n.new('ShaderNodeVolumePrincipled');volume.inputs['Color'].default_value=(.72,.69,.61,1);volume.inputs['Anisotropy'].default_value=.25
geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Position'],sep.inputs[0])
depth=n.new('ShaderNodeMapRange');depth.inputs['From Min'].default_value=-5;depth.inputs['From Max'].default_value=12;depth.inputs['To Min'].default_value=.003;depth.inputs['To Max'].default_value=.018;depth.clamp=True
l.new(sep.outputs['Y'],depth.inputs['Value'])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.23;noise.inputs['Detail'].default_value=2;l.new(geo.outputs['Position'],noise.inputs['Vector'])
variation=n.new('ShaderNodeMapRange');variation.inputs['To Min'].default_value=.75;variation.inputs['To Max'].default_value=1.15;l.new(noise.outputs['Fac'],variation.inputs['Value'])
mult=n.new('ShaderNodeMath');mult.operation='MULTIPLY';l.new(depth.outputs['Result'],mult.inputs[0]);l.new(variation.outputs['Result'],mult.inputs[1]);l.new(mult.outputs[0],volume.inputs['Density']);l.new(volume.outputs['Volume'],out.inputs['Volume'])
bpy.ops.mesh.primitive_cube_add(size=1,location=(-7,4,1.65));o=bpy.context.object;o.name='Concourse atmospheric haze volume'
for c in list(o.users_collection):c.objects.unlink(o)
collection.objects.link(o);o.dimensions=(40,32,3.3);o.display_type='WIRE';o.data.materials.append(material)
scene.cycles.volume_bounces=2
scene['atmosphere']='Thin warm dust haze, density 0.003 near camera to 0.018 in the distance, with gentle static variation.'
folder=os.path.join(os.path.dirname(bpy.data.filepath),'pan-720-7s-haze-frames');os.makedirs(folder,exist_ok=True);scene.render.filepath=os.path.join(folder,'frame-')
scene.frame_set(84)
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'haze':scene['atmosphere'],'file':bpy.data.filepath}
