"""Small deterministic modeling helpers for editable Blender reconstructions."""
import bpy, math, random
from mathutils import Vector

class SceneBuilder:
    def __init__(self,name,prefix):
        self.scene=bpy.data.scenes.new(name);bpy.context.window.scene=self.scene
        self.prefix=prefix;self.collections={};self.cache={};self.group('Architecture')
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1)
        o=bpy.context.object;self.ico=o.data.copy();bpy.data.objects.remove(o,do_unlink=True)
    def group(self,name):
        if name not in self.collections:
            c=bpy.data.collections.new(self.prefix+' | '+name);self.scene.collection.children.link(c);self.collections[name]=c
        self.current=self.collections[name]
    def mesh(self,name,verts,faces,mat,loc=(0,0,0)):
        m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update()
        if mat:m.materials.append(mat)
        o=bpy.data.objects.new(self.prefix+' | '+name,m);self.current.objects.link(o);o.location=loc
        return o
    def box(self,name,loc,size,mat,bevel=0):
        key=(tuple(size),mat.name if mat else '',bevel)
        mesh=self.cache.get(key)
        if mesh is None:
            corners=[(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]
            verts=[tuple(v*s/2 for v,s in zip(c,size)) for c in corners]
            o=self.mesh(name,verts,[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)],mat,loc)
            self.cache[key]=o.data
        else:
            o=bpy.data.objects.new(self.prefix+' | '+name,mesh);self.current.objects.link(o);o.location=loc
        if bevel:
            m=o.modifiers.new('Worn edge bevel','BEVEL');m.width=bevel;m.segments=2
            o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
        return o
    def cylinder(self,name,a,b,r,mat,vertices=16,r2=None):
        if r2 is None:r2=r
        direction=Vector(b)-Vector(a);h=direction.length
        verts=[(math.cos(i*math.tau/vertices)*radius,math.sin(i*math.tau/vertices)*radius,z) for radius,z in [(r,-h/2),(r2,h/2)] for i in range(vertices)]
        faces=[tuple(reversed(range(vertices))),tuple(range(vertices,2*vertices))]
        faces += [(i,(i+1)%vertices,(i+1)%vertices+vertices,i+vertices) for i in range(vertices)]
        o=self.mesh(name,verts,faces,mat,(Vector(a)+Vector(b))/2);o.rotation_euler=direction.to_track_quat('Z','Y').to_euler()
        for p in o.data.polygons:
            if len(p.vertices)==4:p.use_smooth=True
        return o
    def pipe(self,name,points,r,mat):
        c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=2
        s=c.splines.new('POLY');s.points.add(len(points)-1)
        for p,v in zip(s.points,points):p.co=(*v,1)
        c.materials.append(mat);o=bpy.data.objects.new(self.prefix+' | '+name,c);self.current.objects.link(o)
        return o
    def rock(self,name,loc,size,mat,rough=.1,smooth=False):
        mesh=self.ico.copy();mesh.materials.clear();mesh.materials.append(mat)
        for v in mesh.vertices:v.co*=random.uniform(1-rough,1+rough)
        for p in mesh.polygons:p.use_smooth=smooth
        o=bpy.data.objects.new(self.prefix+' | '+name,mesh);self.current.objects.link(o);o.location=loc;o.scale=size
        o.rotation_euler=[random.uniform(-.2,.2) for _ in range(3)]
        return o
    def material(self,name,color,rough=.75,metal=0,scale=3,bump=.015,stretch=(1,1,1)):
        m=bpy.data.materials.new(self.prefix+' | '+name);m.diffuse_color=(*color,1);m.use_nodes=True
        n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
        g=n.new('ShaderNodeNewGeometry');v=n.new('ShaderNodeVectorMath');v.operation='MULTIPLY';v.inputs[1].default_value=stretch;l.new(g.outputs['Position'],v.inputs[0])
        t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=scale;t.inputs['Detail'].default_value=4;l.new(v.outputs[0],t.inputs['Vector'])
        ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.22;ramp.color_ramp.elements[0].color=(*(c*.35 for c in color),1)
        ramp.color_ramp.elements[1].position=.78;ramp.color_ramp.elements[1].color=(*(min(c*1.45,1) for c in color),1)
        l.new(t.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
        fine=n.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=95;fine.inputs['Detail'].default_value=2;l.new(g.outputs['Position'],fine.inputs['Vector'])
        b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.4;b.inputs['Distance'].default_value=bump;l.new(fine.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
        return m
    def light(self,name,kind,loc,power,color,size=1,target=None):
        d=bpy.data.lights.new(name,kind);d.energy=power;d.color=color
        if kind=='AREA':d.shape='DISK';d.size=size
        elif kind=='POINT':d.shadow_soft_size=size
        o=bpy.data.objects.new(self.prefix+' | '+name,d);self.current.objects.link(o);o.location=loc
        if target:o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
        return o
