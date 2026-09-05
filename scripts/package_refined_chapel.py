"""Share the evaluated scan mesh and finalize delivery cameras without losing the source STL."""
import bpy
from mathutils import Vector
s=bpy.context.scene
statues=[o for o in s.objects if any(t in o.name for t in ['Saint Francis looking toward','Left foreground Franciscan','Right foreground Franciscan','Left altar attendant','Right altar attendant'])]
source=next(o for o in statues if 'Left foreground' in o.name)
deps=bpy.context.evaluated_depsgraph_get();mesh=bpy.data.meshes.new_from_object(source.evaluated_get(deps));mesh.name='Shared museum scan - retained render resolution'
for p in mesh.polygons:
    # Keep a continuous carved-wood finish until a proper painted UV mask exists.
    p.material_index=0
right_material=next(o for o in statues if 'Right foreground' in o.name).data.materials[0]
for o in statues:
    o.modifiers.clear();o.data=mesh
    if 'Right foreground' in o.name:o.material_slots[0].link='OBJECT';o.material_slots[0].material=right_material
original=bpy.data.objects.get('REFINED | SMK Saint Francis source scan')
if original:bpy.data.objects.remove(original,do_unlink=True)
cam=bpy.data.objects['São Francisco - revised frame 8 camera'];cam.rotation_euler=(Vector((0,4.46,3.36))-cam.location).to_track_quat('-Z','Y').to_euler()
c=bpy.data.objects['São Francisco - scanned statue detail'];c.location=(-1.3,-3.2,1.8);c.rotation_euler=(Vector((-2.35,-.2,1.58))-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=48
s.camera=cam
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath,compress=True)
result={'file':bpy.data.filepath,'shared_scan_faces':len(mesh.polygons),'statue_instances':len(statues)}
