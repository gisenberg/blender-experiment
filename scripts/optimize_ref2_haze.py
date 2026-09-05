"""Use physically uniform dust for efficient, stable animation rendering."""
import bpy, os
s=bpy.context.scene
m=bpy.data.materials['Subtle airborne dust - background depth'];n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
out=n.new('ShaderNodeOutputMaterial');scatter=n.new('ShaderNodeVolumeScatter');scatter.inputs['Color'].default_value=(.72,.69,.61,1);scatter.inputs['Density'].default_value=.007;scatter.inputs['Anisotropy'].default_value=.25;l.new(scatter.outputs['Volume'],out.inputs['Volume'])
s['atmosphere']='Thin, uniform warm dust haze at density 0.007; optical depth naturally increases along longer sightlines.'
s.cycles.samples=64;s.cycles.adaptive_min_samples=16;s.cycles.adaptive_threshold=.025
s.render.filepath=os.path.join(os.path.dirname(bpy.data.filepath),'pan-final-frames','frame-');os.makedirs(os.path.dirname(s.render.filepath),exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'atmosphere':s['atmosphere']}
