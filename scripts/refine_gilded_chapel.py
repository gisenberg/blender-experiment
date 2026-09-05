"""Increase carving density and tune the first rendered chapel approximation."""
import bpy, math, random, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from scene_helpers import SceneBuilder
s=bpy.context.scene;random.seed(23)
b=SceneBuilder.__new__(SceneBuilder);b.scene=s;b.prefix='Chapel';b.cache={};b.collections={}
b.ico=next(o.data for o in s.objects if 'Saint halo' not in o.name and o.type=='MESH' and 'Rosette boss' in o.name) if any('Rosette boss' in o.name for o in s.objects) else bpy.data.objects[next(o.name for o in s.objects if 'Ceiling gilt boss' in o.name)].data
gold=bpy.data.materials['Chapel | Aged warm gold leaf'];bright=bpy.data.materials['Chapel | Polished raised gilding'];dark=bpy.data.materials['Chapel | Recessed bronze gold'];wood=bpy.data.materials['Chapel | Deep umber carving recess'];skin=bpy.data.materials['Chapel | Polychrome sculpture skin']
for m,color,rough in [(gold,(.39,.245,.11),.43),(bright,(.53,.355,.17),.35),(dark,(.12,.066,.025),.58)]:
    m.diffuse_color=(*color,1);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=rough
    for n in m.node_tree.nodes:
        if n.type=='VALTORGB':
            n.color_ramp.elements[0].color=(*(v*.54 for v in color),1);n.color_ramp.elements[1].color=(*(v*1.15 for v in color),1)
        if n.type=='BUMP':n.inputs['Distance'].default_value=.0025
def leaf(a,c,w,mat=gold):
    a=Vector(a);c=Vector(c);d=c-a;side=Vector((d.z,0,-d.x)).normalized();verts=[]
    for i in range(13):
        t=i/12;mid=a+d*t;width=w*math.sin(math.pi*t)*(.78+.22*math.cos(t*math.pi*8))
        for v in [-1,0,1]:verts.append(tuple(mid+side*width*v+Vector((0,-.025*math.sin(math.pi*t)*(1-.7*abs(v)),0))))
    o=b.mesh('Small serrated acanthus leaf',verts,[(i*3+j,i*3+j+1,(i+1)*3+j+1,(i+1)*3+j) for i in range(12) for j in range(2)],mat)
    for p in o.data.polygons:p.use_smooth=True
def scroll(x,y,z,r,sign):
    pts=[(x+sign*r*(1-.91*i/36)*math.cos(i/36*math.tau*1.3),y,z+r*(1-.91*i/36)*math.sin(i/36*math.tau*1.3)) for i in range(37)]
    b.pipe('Fine undercut scroll',pts,.009,gold)
    leaf((x+sign*r,y,z),(x+sign*r*.5,y-.01,z+r*.9),r*.35,bright)
b.current=bpy.data.collections['Chapel | Carved panel master']
for row in range(9):
    z=-.9+row*.22
    for col in range(5):
        x=-.56+col*.28;sign=1 if (row+col)%2 else -1
        scroll(x,-.21,z,.10,sign)
        leaf((x,-.19,z-.1),(x+sign*.1,-.22,z+.12),.047)
# Add fine fronds around the prominent large scrolls.
for sign in [-1,1]:
    for z in [-.63,0,.63]:
        for i in range(9):
            a=i*math.tau/9;x=sign*.36+math.cos(a)*.265;zz=z+math.sin(a)*.265
            leaf((x,-.19,zz),(x+math.cos(a)*.11,-.22,zz+math.sin(a)*.11),.047,bright)
b.group('Additional dense column foliage')
for x in [-2.45,-1.68,1.68,2.45]:
    for j in range(37):
        z=1.98+j*.137
        for k in range(4):
            a=j*.43+k*math.tau/4;xx=x+math.cos(a)*.23;yy=4.91+math.sin(a)*.23
            leaf((xx,yy,z),(xx+math.cos(a)*.10,yy-.014,z+.18),.075,gold if j%3 else bright)
    for z in [2.4,3.5,4.6,5.7]:
        for sign in [-1,1]:scroll(x+sign*.11,4.62,z,.10,sign)
# A few small facial features clarify the sculptural silhouettes.
b.group('Statue carved facial features')
for o in list(s.objects):
    if o.type!='MESH' or not o.name.endswith(' head'):continue
    x,y,z=o.location;h=o.scale.z/.12
    for sign in [-1,1]:
        eye=b.rock('Carved statue eye',(x+sign*.030*h,y-.079*h,z+.025*h),(.008*h,.004*h,.006*h),wood,0,True)
        b.pipe('Statue brow',[(x+sign*.018*h,y-.078*h,z+.045*h),(x+sign*.042*h,y-.072*h,z+.047*h)],.003*h,wood)
    b.pipe('Carved mouth',[(x-.022*h,y-.080*h,z-.041*h),(x+.021*h,y-.080*h,z-.041*h)],.0025*h,wood)
    for k in range(6):
        xx=x+(.012*k-.03)*h;b.pipe('Sculpted beard fold',[(xx,y-.075*h,z-.045*h),(x+(xx-x)*.6,y-.064*h,z-.11*h)],.005*h,wood)
cam=s.camera;cam.location=(0,-7.1,1.73);cam.rotation_euler=(Vector((0,4.4,3.47))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=28
for o in s.objects:
    if o.name.startswith('Rear tall relief field'):o.hide_render=True;o.hide_set(True)
    if 'Central heavenly figure' in o.name or 'Spread carved wing feather' in o.name:
        if o.type=='MESH':o.data.materials.clear();o.data.materials.append(gold)
s.view_settings.exposure=-1.05
for o in s.objects:
    if o.type=='LIGHT' and o.name.endswith('Altar warm overhead'):o.data.energy=135
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'file':bpy.data.filepath,'objects':len(s.objects)}
