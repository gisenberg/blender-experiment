"""Procedural, editable approximation of the chapel in fDltPLFdkYI at 8 s."""
import bpy, math, random, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from scene_helpers import SceneBuilder
random.seed(83)
b=SceneBuilder('Frame 8 - Gilded baroque chapel','Chapel');s=b.scene
OUT=ROOT/'outputs'/'polyphia-room';OUT.mkdir(parents=True,exist_ok=True)
def material(name,c,metal=0,rough=.4):
    m=b.material(name,c,rough,metal,scale=7,bump=.0007)
    for n in m.node_tree.nodes:
        if n.type=='VALTORGB':
            n.color_ramp.elements[0].color=(*(v*.65 for v in c),1)
            n.color_ramp.elements[1].color=(*(min(v*1.2,1) for v in c),1)
    return m
gold=material('Aged warm gold leaf',(.57,.31,.086),.78,.32)
bright=material('Polished raised gilding',(.74,.47,.17),.83,.25)
darkgold=material('Recessed bronze gold',(.20,.095,.025),.6,.5)
wood=material('Deep umber carving recess',(.047,.022,.009),.15,.65)
stone=material('Warm limestone',(.26,.20,.12),0,.7)
teal=material('Altar faded teal paint',(.039,.15,.145),.13,.47)
ivory=material('Pale carved ivory',(.59,.49,.31),.2,.45)
robe=material('Saint dark brown robe',(.06,.025,.012),0,.76)
skin=material('Polychrome sculpture skin',(.30,.17,.088),0,.6)
black=material('Dark church furniture',(.018,.014,.009),.12,.45)
wax=material('Old ivory candles',(.68,.62,.44),0,.6)
def orb(name,p,scale,mat):
    o=b.rock(name,p,scale,mat,0,True);return o
def ring(name,x,y,z,r,thick,mat=gold):
    return b.pipe(name,[(x+r*math.cos(i*math.tau/48),y,z+r*math.sin(i*math.tau/48)) for i in range(49)],thick,mat)
def leaf(name,a,c,width,mat=gold):
    a=Vector(a);c=Vector(c);d=c-a;side=Vector((d.z,0,-d.x)).normalized();verts=[]
    for i in range(9):
        t=i/8;mid=a+d*t;w=width*math.sin(math.pi*t)**.8
        for v in [-1,0,1]:verts.append(tuple(mid+side*w*v+Vector((0,-.07*math.sin(math.pi*t)*(1-.65*abs(v)),0))))
    o=b.mesh(name,verts,[(3*i+j,3*i+j+1,3*(i+1)+j+1,3*(i+1)+j) for i in range(8) for j in range(2)],mat)
    for p in o.data.polygons:p.use_smooth=True
    return o
def scroll(x,y,z,r=.22,flip=1):
    pts=[]
    for i in range(45):
        t=i/44;angle=t*math.tau*1.32;rad=r*(1-.90*t)
        pts.append((x+flip*math.cos(angle)*rad,y-.025*math.sin(t*math.pi),z+math.sin(angle)*rad))
    b.pipe('Carved volute spiral',pts,.025,gold)
    leaf('Acanthus curled tip',(x+flip*r,y,z),(x+flip*r*.65,y-.01,z+r*.8),r*.26,bright)
def flower(x,y,z,r=.15):
    for k in range(8):
        a=k*math.tau/8;leaf('Rosette petal',(x,y,z),(x+math.cos(a)*r,y,z+math.sin(a)*r),r*.22,bright)
    orb('Rosette boss',(x,y-.04,z),(r*.22,.04,r*.22),gold)
def frame(x,y,z,w,h):
    for j in range(3):
        off=j*.035;mat=[darkgold,gold,bright][j]
        for xx in [x-w/2+off,x+w/2-off]:b.box('Gilded frame upright',(xx,y-j*.025,z),(.04,.08,h-2*off),mat,.008)
        for zz in [z-h/2+off,z+h/2-off]:b.box('Gilded frame rail',(x,y-j*.025,zz),(w-2*off,.08,.04),mat,.008)
    for xx in [x-w/2,x+w/2]:
        for zz in [z-h/2,z+h/2]:flower(xx,y-.08,zz,.11)

# One highly layered carving panel, reused as linked collection instances.
b.group('Carved panel master');panel=b.current
b.box('Panel shadowed backing',(0,.03,0),(1.5,.12,2.14),wood,.015)
frame(0,-.05,0,1.46,2.08)
for sign in [-1,1]:
    for zz in [-.63,0,.63]:
        scroll(sign*.36,-.18,zz,.27,sign)
        leaf('Rising acanthus leaf',(sign*.08,-.15,zz-.25),(sign*.31,-.2,zz+.30),.11)
        leaf('Outward acanthus leaf',(sign*.29,-.15,zz-.15),(sign*.62,-.17,zz+.10),.10,bright)
    b.pipe('Flowing carved stem',[(sign*(.1+.11*math.sin(i*.23)),-.14,-.98+i*.065) for i in range(31)],.021,gold)
for z in [-.79,-.22,.37,.89]:flower(0,-.21,z,.16)
s.collection.children.unlink(panel)
def instance(name,collection,loc,rot=0,scale=(1,1,1)):
    o=bpy.data.objects.new(name,None);o.instance_type='COLLECTION';o.instance_collection=collection;b.current.objects.link(o);o.location=loc;o.rotation_euler.z=rot;o.scale=scale;return o

b.group('Chapel shell and stepped floor')
b.box('Rear wall',(0,5.4,4),(6.4,.35,8),wood)
b.box('Left wall',(-3.15,0,4),(.22,10.8,8),wood)
b.box('Right wall',(3.15,0,4),(.22,10.8,8),wood)
b.box('Coffered ceiling',(0,0,8.05),(6.4,10.8,.2),wood)
floor2=material('Dark limestone inlay',(.14,.09,.042),0,.7)
for ix in range(12):
    for iy in range(22):b.box('Stone floor tile',(-2.9+ix*.52,-5.4+iy*.5,-.04),(.515,.495,.075),stone if (ix+iy)%4 else floor2,.003)
for j in range(4):
    b.box('Sanctuary step',(0,3.13+j*.25,.08+j*.13),(5.4-j*.16,3.4-j*.5,.16),stone,.018)
    b.box('Step gilt nosing',(0,1.43+j*.5,.15+j*.13),(5.4-j*.16,.035,.025),darkgold,.005)
b.group('Repeated side-wall relief panels')
for side in [-1,1]:
    rot=math.pi/2 if side<0 else -math.pi/2
    for y in [-4.2,-2.55,-.90,.75,2.40,4.05]:
        for z in [1.28,3.52,6.72]:instance('Linked deep acanthus relief',panel,(side*3.0,y,z),rot,scale=(1,1,.91 if z>5 else 1))
    for z in [.18,2.42,4.68,5.01,7.85]:
        for j in range(3):b.box('Continuous side cornice',(side*(3.0-j*.025),0,z+j*.045),(.10+j*.02,10.7,.055),[darkgold,gold,bright][j],.008)
        for i in range(130):orb('Cornice bead',(side*2.94,-5.2+i*.08,z+.08),(.025,.025,.025),bright)
    for y in [-5.04,-3.4,-1.74,-.08,1.57,3.22,4.88]:
        for z in [1.2,3.45,6.8]:
            # Narrow divider composed of overlapping small leaf bosses.
            for k in range(12):
                pos=(side*2.89,y,z-.9+k*.15);orb('Carved divider bead',pos,(.09,.075,.11),gold)
    # Recessed framed religious panels at upper eye level.
    for y in [-3.3,-.55,2.2]:
        col=bpy.data.collections.new('Framed sacred panel');saved=b.current;b.current=col
        paint=material('Painted panel '+str(side)+str(y),(.078,.035,.021),0,.9)
        b.box('Old painted panel',(0,.01,0),(1.7,.035,1.18),paint)
        frame(0,-.04,0,1.84,1.31)
        # Stylized low relief painted figures, subordinate to the architectural reconstruction.
        for n,x in enumerate([-.47,0,.45]):
            pm=[robe,teal,ivory][n];orb('Painted saint head',(x,-.04,.19),(.095,.013,.12),skin)
            b.mesh('Painted drapery',[(x-.18,-.035,-.49),(x+.20,-.035,-.49),(x+.10,-.035,.12),(x-.08,-.035,.12)],[(0,1,2,3)],pm)
            ring('Painted halo',x,-.05,.20,.135,.01,darkgold)
        b.current=saved;instance('Framed sacred wall panel',col,(side*2.92,y,5.57),rot)

def column(x,y,z,height,r=.22):
    b.cylinder('Carved column shadow core',(x,y,z),(x,y,z+height),r*.78,darkgold,32)
    for h,rad in [(0,r*1.5),(.08,r*1.6),(.18,r*1.25),(height-.32,r*1.20),(height-.17,r*1.6),(height-.06,r*1.8)]:
        b.cylinder('Column moulded collar',(x,y,z+h),(x,y,z+h+.075),rad,gold,40)
    for phase in [0,math.pi]:
        pts=[(x+r*math.cos(phase+i/100*math.tau*3),y+r*math.sin(phase+i/100*math.tau*3),z+.2+i/100*(height-.52)) for i in range(101)]
        b.pipe('Spiral gilded column vine',pts,.055,gold)
        for i in range(0,100,4):
            px,py,pz=pts[i];orb('Column vine leaf',(px,py,pz),(.095,.07,.15),gold)
    for k in range(8):
        a=k*math.tau/8;orb('Corinthian capital leaf',(x+math.cos(a)*r*1.15,y+math.sin(a)*r*1.15,z+height-.26),(.14,.13,.20),bright)
    for zz in [z-.1,z+height+.05]:b.box('Column square abacus',(x,y,zz),(r*3.4,r*3.2,.14),gold,.025)

b.group('Altar retable and architectural columns')
for x in [-2.45,-1.68,1.68,2.45]:
    b.box('Column ornamented plinth',(x,4.78,1.03),(.65,.68,1.08),darkgold,.025)
    instance('Plinth relief',panel,(x,4.40,1.02),scale=(.40,.6,.45))
    column(x,4.91,1.68,5.65,.24)
for x in [-2.9,2.9]:
    for y in [-2.9,.0,2.9]:column(x,y,4.95,2.7,.13)
for x in [-.82,.82]:instance('Rear tall relief field',panel,(x,5.14,4.50),scale=(.91,1,2.12))
b.box('Central luminous gilt niche',(0,5.13,4.48),(2.34,.09,4.95),gold,.04)
for row in range(20):
    for col in range(10):
        x=-1.04+col*.23;z=2.30+row*.235
        ring('Niche brocade lozenge',x,5.04,z,.072,.008,bright)
        if (row+col)%2==0:orb('Niche flower stud',(x,5.015,z),(.026,.013,.036),ivory)
for z in [7.25,7.43,7.59,7.76]:
    b.box('Rear monumental entablature',(0,5.00,z),(6.1,.72,.13),gold,.015)
    for x in [-2.45,-1.68,1.68,2.45]:b.box('Projecting entablature block',(x,4.68,z),(.72,.97,.12),bright,.012)
for x in [-2.64+i*.15 for i in range(36)]:b.box('Entablature dentil',(x,4.65,7.33),(.075,.11,.10),bright,.008)
# Tiered tabernacle and bowed teal altar frontal.
for j in range(6):
    w=2.48-j*.30;y=4.40+j*.05;z=1.47+j*.28
    b.box('Gilded tabernacle tier',(0,y,z),(w,.76,.26),gold,.025)
    b.box('Tabernacle tier projecting lip',(0,y-.06,z+.12),(w+.12,.9,.055),bright,.009)
b.box('Altar table top',(0,3.86,1.56),(3.65,1.1,.15),gold,.035)
verts=[]
for z,w,y in [(.55,2.60,3.28),(.76,2.95,3.13),(1.40,3.46,3.10),(1.49,3.50,3.14)]:verts.extend([(-w/2,y,z),(w/2,y,z)])
o=b.mesh('Bowed teal altar frontal',verts,[(0,1,3,2),(2,3,5,4),(4,5,7,6)],teal)
for sign in [-1,1]:b.pipe('Altar curling gilt edge',[(sign*1.3,3.24,.56),(sign*1.42,3.11,.77),(sign*1.58,3.06,1.07),(sign*1.73,3.09,1.46)],.07,gold)
for x in [-1.13,-.58,0,.58,1.13]:
    scroll(x,3.08,1.11,.15,1 if x>=0 else -1);leaf('Altar gilded spray',(x,3.07,.68),(x+.17,3.04,1.4),.09,bright)
for x in [-2.7,2.7]:instance('Side altar block carving',panel,(x,3.78,1.25),scale=(.45,1,.65))

def statue(name,x,y,z,h=1.4,cloth=robe):
    # Fluted garment mesh, sculpted head, bent arms, and hands.
    verts=[];segments=40
    for j,(height,r) in enumerate([(0,.23),(.16,.21),(.55,.15),(.81,.20),(.88,.08)]):
        for k in range(segments):
            a=k*math.tau/segments;rr=r*(1+.14*math.cos(a*9+j*.15));verts.append((x+h*rr*math.cos(a),y+h*rr*.65*math.sin(a),z+h*height))
    ob=b.mesh(name+' deeply folded robe',verts,[(j*segments+k,j*segments+(k+1)%segments,(j+1)*segments+(k+1)%segments,(j+1)*segments+k) for j in range(4) for k in range(segments)],cloth)
    for p in ob.data.polygons:p.use_smooth=True
    orb(name+' head',(x,y-.016*h,z+.96*h),(.092*h,.083*h,.12*h),skin)
    orb(name+' carved hair',(x,y+.016*h,z+1.0*h),(.100*h,.085*h,.095*h),wood)
    orb(name+' nose',(x,y-.096*h,z+.96*h),(.024*h,.025*h,.04*h),skin)
    for sign in [-1,1]:
        shoulder=(x+sign*.17*h,y,z+.78*h);elbow=(x+sign*.22*h,y-.13*h,z+.59*h);hand=(x+sign*.07*h,y-.20*h,z+.66*h)
        b.cylinder(name+' upper sleeve',shoulder,elbow,.055*h,cloth,20)
        b.cylinder(name+' lower sleeve',elbow,hand,.048*h,cloth,20)
        orb(name+' hand',hand,(.033*h,.031*h,.05*h),skin)
    b.pipe(name+' waist cord',[(x+.151*h*math.cos(i*math.tau/40),y+.104*h*math.sin(i*math.tau/40),z+.57*h) for i in range(41)],.008*h,gold)
    return ob

b.group('Polychrome saints and devotional pedestals')
statue('Central niche saint',-.34,4.50,3.14,1.42,robe)
statue('Small tabernacle figure',0,3.98,2.25,.62,ivory)
for sign in [-1,1]:
    for y,h in [(-.22,1.25),(2.68,.96)]:
        x=sign*2.35
        for j in range(4):b.box('Saint pedestal moulding',(x,y,.19+j*.10),(.8-j*.07,.72-j*.04,.10),gold,.026)
        instance('Saint pedestal acanthus',panel,(x,y-.36,.44),scale=(.5,.7,.33))
        statue('Side wall saint',x,y,.59,h,robe if sign<0 else teal)
        # Decorative radiating halo behind each head.
        ring('Saint halo',x,y+.055,.59+h, h*.15,.016,bright)
for sign in [-1,1]:
    statue('Gilded attendant',sign*1.95,4.12,1.76,.80,gold)

b.group('Sunburst and winged heavenly figure')
cx,cy,cz=0,4.54,6.78
for i in range(64):
    a=i*math.tau/64;r0=.26;r1=1.20+random.random()*.36;w=.018 if i%3 else .045
    verts=[(cx+math.cos(a)*r0,cy,cz+math.sin(a)*r0),(cx+math.cos(a)*r1,cy-.03,cz+math.sin(a)*r1),(cx+math.cos(a+w)*r0,cy,cz+math.sin(a+w)*r0)]
    b.mesh('Long gilded sun ray',verts,[(0,1,2)],bright if i%3 else gold)
statue('Central heavenly figure',0,4.18,6.25,.77,ivory)
for sign in [-1,1]:
    for k in range(16):
        t=k/15;a=(sign*.1,4.22,6.86);end=(sign*(.65+t*.62),4.25,6.89+.65*math.sin(t*1.6))
        leaf('Spread carved wing feather',a,end,.055,ivory)
    leaf('Large descending wing feather',(sign*.12,4.17,6.87),(sign*.23,4.17,5.94),.14,gold)

b.group('Candlesticks and dark sanctuary chairs')
def candle(x,y,z,height=.7):
    b.cylinder('Candleholder wide base',(x,y,z),(x,y,z+.07),.11,gold,32)
    b.cylinder('Candleholder stem',(x,y,z+.07),(x,y,z+.37),.025,bright,24)
    for zz,r in [(z+.15,.06),(z+.30,.055),(z+.39,.09)]:b.cylinder('Candleholder turned collar',(x,y,zz),(x,y,zz+.045),r,gold,24)
    b.cylinder('Ivory wax taper',(x,y,z+.435),(x,y,z+.435+height),.026,wax,24)
for x in [-1.40,-1.12,1.12,1.40]:candle(x,3.95,1.63,.66)
for side in [-1,1]:
    for y in [-2.8,.85,3.32]:
        x=side*2.74
        b.pipe('Wall candle bracket',[(side*3,y,2.88),(side*2.66,y,2.88),(side*2.63,y,3.15)],.035,gold)
        candle(side*2.63,y,3.12,1.04)
    for y in [2.2,2.8]:
        x=side*2.10
        b.box('Dark carved chair seat',(x,y,.65),(.42,.4,.1),black,.03)
        for xx in [x-.17,x+.17]:
            for yy in [y-.15,y+.15]:b.cylinder('Chair cabriole leg',(xx,yy,.1),(xx,yy,.62),.026,black,16)
        b.box('Chair tall carved back',(x,y+.16,1.03),(.39,.065,.69),black,.05)
        for xx in [x-.2,x+.2]:orb('Chair finial',(xx,y+.16,1.43),(.046,.046,.08),black)

b.group('Ceiling coffers and overhead scrolls')
for x in [-2.5,-1.25,0,1.25,2.5]:b.box('Coffered ceiling longitudinal beam',(x,0,7.92),(.14,10.7,.14),gold,.015)
for y in [-4.8,-3.2,-1.6,0,1.6,3.2,4.8]:b.box('Coffered ceiling transverse beam',(0,y,7.9),(6.1,.15,.16),gold,.015)
for x in [-1.95,-.65,.65,1.95]:
    for y in [-4,-2.4,-.8,.8,2.4,4]:orb('Ceiling gilt boss',(x,y,7.87),(.15,.15,.08),bright)

b.group('Warm chapel lighting and matched camera')
w=bpy.data.worlds.new('Chapel dark ambient');s.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.28,.20,.11,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.10
b.light('Soft warm frontal bounce','AREA',(0,-3.9,5.1),310,(1,.76,.46),4.0,(0,4.8,3.7))
b.light('Altar warm overhead','AREA',(0,3.20,6.9),220,(1,.76,.43),2.2,(0,4.5,2.3))
for sign in [-1,1]:
    b.light('High side window daylight','AREA',(sign*2.78,-1.2,6.6),210,(1,.87,.64),2.2,(0,2.5,2.9))
    b.light('Sculpture fill','AREA',(sign*1.8,-1.7,3.5),35,(1,.68,.34),1.3,(sign*2.5,.7,1.8))
d=bpy.data.cameras.new('Frame 8 matched camera');cam=bpy.data.objects.new('Frame 8 matched camera',d);b.current.objects.link(cam)
cam.location=(0,-5.3,1.78);target=Vector((0,4.40,3.77));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();d.lens=27;s.camera=cam
s.render.engine='CYCLES';s.cycles.samples=128;s.cycles.use_denoising=True;s.cycles.max_bounces=8
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for dev in prefs.devices:dev.use=dev.type=='OPTIX'
s.cycles.device='GPU';s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
s.render.filepath=str(OUT/'gilded-chapel-still.png');s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-.65
s['reference_url']='https://www.youtube.com/watch?v=fDltPLFdkYI&t=8s';s['reference_time_seconds']=8
s['reconstruction_scope']='Editable architectural approximation from one frame. Carved ornament and sacred figures are procedural interpretations; dimensions and hidden surfaces are inferred. Foreground performer omitted.'
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.overlay.show_overlays=False
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'gilded-chapel-reconstruction.blend'))
result={'file':bpy.data.filepath,'objects':len(s.objects),'scene':s.name}
