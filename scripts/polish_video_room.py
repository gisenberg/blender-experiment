"""Refine silhouettes, textiles, and framing after rendered inspection."""
import bpy, math, random, sys
from pathlib import Path
from mathutils import Vector,Quaternion
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from scene_helpers import SceneBuilder
s=bpy.context.scene;random.seed(29)
for m in bpy.data.materials:
    if not m.name.startswith('Music room | '):continue
    if any(k in m.name for k in ['woven sofa','guitar spruce','oak floor']):
        base=m.diffuse_color[:3]
        for n in m.node_tree.nodes:
            if n.type=='VALTORGB':
                n.color_ramp.elements[0].color=(*(c*.75 for c in base),1)
                n.color_ramp.elements[1].color=(*(c*1.1 for c in base),1)
for o in s.objects:
    if 'Small oval desktop speaker' in o.name:o.location.x=1.98;o.location.z=.86
    if 'Speaker power LED' in o.name:o.location.x=1.905;o.location.z=.88
    if 'Glossy curved rubber leaf' in o.name:
        vs=o.data.vertices;start=vs[1].co.copy();end=vs[-2].co.copy();axis=(end-start).normalized()
        q=Quaternion(axis,random.choice([-1,1])*random.uniform(.5,1.2))
        for v in vs:
            delta=v.co-start;along=axis*delta.dot(axis);across=delta-along
            v.co=start+q@(along+across*1.6)
    if o.type=='MESH' and 'carved body' in o.name:
        old=o.data;n=len(old.vertices)//2;front=[v.co.copy() for v in old.vertices[:n]];back=[v.co.copy() for v in old.vertices[n:]]
        def smooth(points):
            out=[]
            for i in range(len(points)):
                p0,p1,p2,p3=[points[j%len(points)] for j in [i-1,i,i+1,i+2]]
                for k in range(6):
                    t=k/6;out.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
            return out
        verts=smooth(front)+smooth(back);n=len(verts)//2
        mesh=bpy.data.meshes.new('Smooth carved instrument silhouette');mesh.from_pydata(verts,[],[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)])
        for m in old.materials:mesh.materials.append(m)
        o.data=mesh
    if 'Soft filming light' in o.name:o.data.energy=42
    if 'reconstructed wide view' in o.name:
        o.location=(-.25,-3.5,1.65);o.rotation_euler=(Vector((.03,.9,.95))-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=32
o=next(o for o in s.objects if 'Woven repeating kilim diamonds' in o.name)
materials=list(o.data.materials);verts=[];faces=[];colors=[]
for row in range(40):
    for col in range(40):
        x=-.40+col*.052;y=-.65+row*.060;v=len(verts)
        verts.extend([(x,y,.016),(x+.052,y,.016),(x+.052,y+.060,.016),(x,y+.060,.016)])
        faces.append((v,v+1,v+2,v+3))
        if row%10 in [0,1]:color=2 if row%10==0 else 4
        else:
            zig=abs((col%10)-5);r=row%10
            color=2 if abs(r-5)==zig//2 or abs(r-5)==zig//2+1 else (1 if (row//10)%2 else 0)
        if col in [0,1,38,39]:color=4 if col in [1,38] else 2
        colors.append(color)
mesh=bpy.data.meshes.new('Stepped traditional kilim bands');mesh.from_pydata(verts,[],faces)
for m in materials:mesh.materials.append(m)
for p,i in zip(mesh.polygons,colors):p.material_index=i
o.data=mesh
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'file':bpy.data.filepath,'refinements':'Smoothed guitars, broad glossy leaves, woven kilim bands, subdued fabric and wider framing'}
