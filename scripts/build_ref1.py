"""Editable reconstruction of the hazy service yard in ref-1.jpg."""
import bpy, math, random, os, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from scene_helpers import SceneBuilder
random.seed(104)
OUT=ROOT/'outputs'/'ref-1';OUT.mkdir(parents=True,exist_ok=True)
b=SceneBuilder('Ref 1 - Hazy abandoned service yard','R1');scene=b.scene
box=b.box;cyl=b.cylinder;pipe=b.pipe;rock=b.rock
concrete=b.material('Chipped pale concrete',(.38,.37,.32),scale=1.6,bump=.012)
asphalt=b.material('Coarse cracked asphalt',(.105,.112,.109),rough=.96,scale=1,bump=.025)
paving=b.material('Dusty sidewalk blocks',(.30,.30,.25),scale=4,bump=.009)
mortar=b.material('Mortar and road cracks',(.045,.045,.035),bump=.005)
tan=b.material('Weathered sand colored siding',(.34,.28,.18),rough=.83,stretch=(1,1,.15),bump=.01)
trim=b.material('Dark structural galvanized metal',(.14,.18,.18),rough=.62,metal=.65,bump=.006)
silver=b.material('Aged pale galvanized flashing',(.48,.51,.46),rough=.53,metal=.5,bump=.008)
blue=b.material('Faded blue steel with grime',(.055,.20,.28),rough=.72,metal=.4,scale=1.7,bump=.013)
bluelight=b.material('Oxidized blue corrugation',(.09,.25,.32),rough=.78,metal=.4,bump=.012)
rust=b.material('Rust and exposed iron',(.14,.068,.023),rough=.9,metal=.3,scale=2,bump=.015)
wood=b.material('Aged bare timber',(.23,.17,.10),stretch=(1,1,.15),scale=3,bump=.014)
card=b.material('Dirty corrugated cardboard',(.40,.30,.16),rough=.96,scale=3,bump=.006)
black=b.material('Charred rubber and bin liners',(.014,.016,.015),rough=.7,scale=6,bump=.013)
glass=b.material('Dusty black glass',(.07,.105,.11),rough=.23,metal=.35,bump=.001)
red=b.material('Faded fire engine vermilion',(.36,.075,.028),rough=.58,metal=.35,scale=2,bump=.008)
ivory=b.material('Old ivory painted metal',(.62,.61,.49),rough=.7,metal=.18,bump=.006)
wall=b.material('Apartment stucco',(.47,.46,.39),rough=.92,scale=.7,bump=.01)
balcony=b.material('Concrete balcony dividers',(.60,.59,.51),scale=2,bump=.006)
leaf=b.material('Dusty olive leaves',(.17,.22,.075),rough=.95,scale=4,bump=.015)
cloth=b.material('Discarded faded work clothes',(.12,.15,.17),rough=1,bump=.008)
paper=b.material('Scattered dirty paper',(.55,.53,.41),rough=1,bump=.002)
white=b.material('Faded white graffiti',(.68,.71,.61),rough=.9,bump=.001)

# Asphalt, pavements and dark cracks.
b.group('Ground and roads')
box('Asphalt yard',(0,5,-.18),(65,80,.30),asphalt)
box('Workshop sidewalk',(-5,2,.02),(13,9,.16),mortar)
for x in range(-26,1):
    for y in range(-5,13):box('Sidewalk paving block',(x*.44,y*.44,.112),(.433,.433,.065),paving)
for y in range(-17,22):
    box('Right road kerb',(14,y,.015),(.23,.984,.20),concrete,.018)
for x in range(-12,1):box('Front workshop kerb',(x,-2.35,.06),(.984,.23,.22),concrete,.018)
for i in range(18):
    x=random.uniform(-10,16);y=random.uniform(-17,17);pts=[(x,y,-.016)]
    for j in range(random.randint(5,12)):
        x+=random.uniform(-.4,.4);y+=random.uniform(.15,.6);pts.append((x,y,-.015))
    pipe('Jagged asphalt fracture',pts,random.uniform(.007,.022),mortar)

# The tan two-storey utility buildings.
b.group('Utility buildings')
box('Long prefab workshop body',(0,9,3.2),(18,6.5,6.4),tan)
box('Long low pale sheet roof',(0,9,6.44),(18.4,6.9,.15),silver,.015)
for z in [i*.14+.15 for i in range(45)]:box('Horizontal facade siding seam',(0,5.735,z),(18,.027,.017),rust)
for x in [-9,-6,-3,0,3,6,9]:box('Workshop facade vertical trim',(x,5.67,3.2),(.09,.12,6.5),trim,.008)
def window(name,x,y,z,w=1.05,h=1.55):
    box(name+' recess',(x,y+.025,z),(w+.10,.12,h+.10),trim,.015)
    box(name+' glass',(x,y-.048,z),(w,.035,h),glass)
    for xx in [x-w/2,x,x+w/2]:box(name+' vertical frame',(xx,y-.08,z),(.037,.065,h+.06),ivory,.003)
    for zz in [z-h/2,z+h/2]:box(name+' sill',(x,y-.08,zz),(w+.08,.10,.05),ivory,.004)
for x in [-7.5,-5.3,-3.1]:window('Upper workshop window',x,5.65,4.27)
window('Right workshop window',6.8,5.65,4.28,1.45,1.4)
window('Workshop low vent',6.8,5.65,2.3,1.35,.42)
for x,w in [(1.3,7.1),(7.2,3.0)]:
    box('Raised front parapet',(x,5.50,6.72),(w,.2,1.67),silver)
    for xx in [x-w/2,x+w/2]:box('Parapet perimeter steel',(xx,5.36,6.73),(.13,.21,1.8),trim,.012)
    for z in [5.91,7.52]:box('Parapet horizontal coping',(x,5.36,z),(w+.15,.25,.13),trim,.01)
    for zz in [6+i*.125 for i in range(12)]:box('Parapet fine rib',(x,5.375,zz),(w,.04,.018),trim)
    for xx in [x-w/2+i*.6 for i in range(1,int(w/.6))]:box('Parapet vertical stain rib',(xx,5.37,6.75),(.018,.035,1.55),trim)
box('Upper steel access door',(1.1,5.61,4.05),(1.03,.12,2.05),rust,.015)
box('Door handle',(1.49,5.50,4.05),(.04,.08,.15),silver,.008)
box('Upper access landing',(1.1,4.79,3.04),(1.6,1.65,.12),trim)
for i in range(15):
    x=-2.4+i*.22;z=.13+i*.195
    box('External stair open tread',(x,4.36,z),(.25,1.16,.055),silver,.009)
for y in [3.72,5.0]:
    pipe('External stair stringer',[(-2.7,y,-.03),(1.2,y,3.06)],.06,trim)
    pipe('Stair handrail',[(-2.7,y,.83),(-2.3,y,1.0),(1.0,y,3.91),(1.75,y,3.91)],.031,trim)
    for x,z in [(-2.4,.13),(-1.2,1.2),(0,2.3),(1.6,3.07)]:cyl('Stair rail upright',(x,y,z),(x,y,z+.86),.025,trim)
for y in [4.2,5.3]:cyl('Landing support',(1.6,y,1.8),(1.6,y,3.05),.07,trim)
box('Second upper service door',(8.2,5.55,4.0),(.9,.16,1.9),rust)
for i in range(13):box('Second access staircase',(7.4+i*.14,4.9-i*.19,.15+i*.22),(.92,.24,.045),silver,.005)
for x in [6.95,7.88]:pipe('Rear stair handrail',[(x,5.0,1.0),(x+1.8,2.7,3.75)],.025,trim)
for x in [-8.8,-.7,4.8,8.7]:pipe('Roof drainage pipe',[(x,5.48,6.35),(x,5.45,.3),(x+.2,5.1,.15)],.04,trim)

# Blue corrugated construction fence and battered garage.
b.group('Fences and garage')
def fence(name,a,c,height=2.15):
    a=Vector(a);c=Vector(c);delta=c-a;length=delta.length;axis=delta.normalized();normal=Vector((-axis.y,axis.x,0))
    count=int(length/.085)
    verts=[];faces=[]
    for i in range(count+1):
        v=a+axis*(length*i/count)+normal*(.025 if i%2 else -.025)
        verts.extend([(v.x,v.y,0),(v.x,v.y,height)])
    for i in range(count):faces.append((2*i,2*i+2,2*i+3,2*i+1))
    o=b.mesh(name,verts,faces,blue);sol=o.modifiers.new('Steel sheet thickness','SOLIDIFY');sol.thickness=.014
    for i in range(int(length/2)+1):
        v=a+axis*min(i*2,length);cyl('Fence upright',v,(v.x,v.y,height+.12),.035,trim)
    for z in [.35,height-.25]:pipe('Fence rear crossrail',[(a.x,a.y,z),(c.x,c.y,z)],.025,rust)
fence('Main blue construction hoarding',(-3,2.3,0),(8.3,2.3,0))
fence('Hoarding left return',(-3,2.3,0),(-3,5.3,0))
fence('Rear blue fence',(8.3,6.1,0),(18,10.6,0),1.85)
box('Garage concrete shell',(-7,-.2,1.8),(6.0,4.7,3.6),concrete,.025)
box('Garage flat cap roof',(-7,-.2,3.68),(6.25,4.95,.18),concrete,.025)
box('Garage shutter recess',(-7,-2.58,1.6),(4.3,.12,3.15),trim)
for z in [i*.075+.15 for i in range(39)]:box('Garage roller shutter slat',(-7,-2.66,z),(4.12,.09,.052),trim,.006)
for z in [3.25,3.4,3.55]:box('Garage horizontal flashing',(-7,-2.74,z),(6.05,.12,.10),silver,.006)
for x in [-9.85,-4.15]:box('Garage door jamb',(x,-2.65,1.8),(.17,.18,3.55),silver)
font_path=next((p for p in ['C:/Windows/Fonts/arialbd.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'] if os.path.exists(p)),None)
def text(name,string,loc,size,mat,offset=0):
    c=bpy.data.curves.new(name,'FONT');c.body=string;c.size=size;c.extrude=.0005;c.offset=offset
    if font_path:c.font=bpy.data.fonts.load(font_path,check_existing=True)
    o=bpy.data.objects.new('R1 | '+name,c);b.current.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0);c.materials.append(mat)
    return o
text('Garage graffiti dark outline','НИКИТА',(-8.92,-2.728,1.9),.60,black,.027)
text('Garage white graffiti','НИКИТА',(-8.92,-2.74,1.925),.60,white)
green=b.material('Acid yellow paint',(.44,.48,.10),rough=.8,bump=.001)
for i in range(16):
    x=-8.8+i*.22;pipe('Graffiti drips',[(x,-2.75,2.0),(x+.02,-2.75,1.8-random.random()*.17)],.012,green)
for i in range(12):
    x=random.uniform(-.1,2.1);z=random.uniform(.7,1.5)
    pipe('White spraypaint tag',[(x-.18,2.263,z+.22),(x+.13,2.26,z-.13),(x+.30,2.26,z+.35),(x-.22,2.26,z)],.014,white)
for i in range(3):
    o=box('Leaning broken plywood',(-1.7+i*.12,3.52,.61),(.85,.07,1.3),wood,.01);o.rotation_euler=(0,-.32,.15*i)

# Dark near-left building, entrance steps and sagging camouflage netting.
b.group('Left entrance')
box('Near building wall',(-13.0,-2,7),(.65,24,14),trim)
for z in [i*.19 for i in range(72)]:box('Near building horizontal cladding',(-12.60,-2,z),(.1,24,.055),silver)
box('Raised entrance platform',(-10.5,-4.2,.63),(4.4,5.5,1.3),concrete)
for i in range(6):box('Entrance steps',(-8.3,-7.3+i*.36,.10+i*.2),(2.35,.38,.20),concrete,.015)
for x in [-9.45,-7.15]:
    pipe('Entrance stair rail',[(x,-7.65,.8),(x,-5.45,2.05)],.035,silver)
    for y,z in [(-7.5,.16),(-6.3,.82),(-5.5,1.22)]:cyl('Entrance rail post',(x,y,z),(x,y,z+.85),.028,silver)
for x in [-12.3,-10.8,-9.4]:cyl('Platform rail post',(x,-6.9,1.28),(x,-6.9,2.3),.035,rust)
pipe('Platform top rail',[(-12.3,-6.9,2.3),(-9.4,-6.9,2.3)],.035,rust)
for x in [-12.2+i*.16 for i in range(17)]:cyl('Platform railing spindle',(x,-6.9,1.4),(x,-6.9,2.25),.012,rust)
verts=[];faces=[];nx=32;ny=13
for i in range(nx+1):
    u=i/nx
    for j in range(ny+1):
        v=j/ny;verts.append((-12.6+6*u,1+2.7*v,5.7-.8*u-1.05*math.sin(u*math.pi)+.18*math.sin(v*9+u*13)))
for i in range(nx):
    for j in range(ny):
        if random.random()>.26:
            k=i*(ny+1)+j;faces.append((k,k+ny+1,k+ny+2,k+1))
net=b.mesh('Torn sagging camouflage canopy',verts,faces,leaf);s=net.modifiers.new('Ragged net thickness','SOLIDIFY');s.thickness=.012
for i in range(0,nx+1,2):pipe('Camouflage net cords',[verts[i*(ny+1)+j] for j in range(ny+1)],.009,black)

# Open steel rubble skip, with a genuinely modeled interior.
b.group('Skip and rubble')
cx,cy=4.4,-2.2;L,W,H=4.9,2.35,1.95
box('Skip bottom',(cx,cy,.19),(L,W,.16),rust,.015)
for y in [cy-W/2,cy+W/2]:
    box('Skip long blue wall',(cx,y,H/2),(L,.09,H),blue,.015)
    box('Skip long upper rim',(cx,y,H),(L+.13,.14,.13),bluelight,.015)
    for x in [cx-L/2+i*.70 for i in range(8)]:box('Skip welded vertical stiffener',(x,y-.045,H/2),(.075,.14,H),bluelight,.008)
    for z in [.20,1.02]:box('Skip lower horizontal stiffener',(cx,y-.05,z),(L,.12,.075),bluelight,.008)
for x in [cx-L/2,cx+L/2]:
    box('Skip blue end',(x,cy,H/2),(.09,W,H),blue,.01)
    box('Skip end top rim',(x,cy,H),(.15,W+.12,.14),bluelight,.015)
for i in range(32):
    x=cx+random.uniform(-2.2,2.2);y=cy+random.uniform(-.95,.95);z=random.uniform(.8,1.75)
    rock('Concrete demolition chunk',(x,y,z),(random.uniform(.22,.65),random.uniform(.18,.45),random.uniform(.12,.33)),concrete,.25)
for i,(x,y,z,s,ang) in enumerate([(3.1,-2.3,2.0,(2.7,.67,.21),(.15,.14,-.22)),(4.8,-2.1,2.02,(2.2,.65,.23),(-.2,-.13,.3)),(5.7,-2.0,2.13,(1.45,.8,.20),(.2,.3,-.3))]):
    slab=box('Broken reinforced concrete slab',(x,y,z),s,concrete,.04);slab.rotation_euler=ang
    for j in range(4):pipe('Exposed bent reinforcing bar',[(x-.7+j*.24,y,z),(x-.9+j*.24,y+.35,z+.35),(x-.75+j*.24,y+.6,z+.56)],.012,rust)
for i in range(12):
    x=random.uniform(2.2,6.6);pipe('Skip paint scratches',[(x,cy-W/2-.096,.2),(x+.07,cy-W/2-.096,random.uniform(.7,1.7))],.008,rust)

# Wheels and vehicles are modeled as separate editable mechanical parts.
b.group('Vehicles')
def wheel(name,x,y,z,r=.55,width=.32):
    cyl(name+' tire',(x,y-width/2,z),(x,y+width/2,z),r,black,32)
    side=y-width/2-.015 if y<0 else y+width/2+.015
    # Both outward-facing sidewalls receive rusty rims.
    for yy in [y-width/2-.014,y+width/2+.014]:
        cyl(name+' rim',(x,yy-.008,z),(x,yy+.008,z),r*.56,rust,24)
        cyl(name+' hub',(x,yy-.02,z),(x,yy+.02,z),r*.25,trim,20)
        for k in range(8):
            a=k*math.tau/8;cyl(name+' lug bolt',(x+math.cos(a)*r*.39,yy-.024,z+math.sin(a)*r*.39),(x+math.cos(a)*r*.39,yy+.024,z+math.sin(a)*r*.39),.025,silver,8)
    for k in range(28):
        a=k*math.tau/28;o=box(name+' tread lug',(x+math.sin(a)*r,y,z+math.cos(a)*r),(.12,width+.018,.035),black,.007);o.rotation_euler[1]=a

# Foreground blue flatbed trailer, long axis into the yard.
tx,ty=-4.7,-11.7
box('Flatbed heavy underframe',(tx,ty,.76),(3.05,9.8,.22),trim,.03)
box('Flatbed wooden deck',(tx,ty,1.04),(3.18,9.7,.10),wood)
for x in [tx-1.46+i*.105 for i in range(29)]:box('Trailer long galvanized deck plank',(x,ty,1.11),(.095,9.7,.035),bluelight,.002)
for x in [tx-1.62,tx+1.62]:
    for z in [.83,.95,1.07]:box('Blue trailer corrugated side',(x,ty,z),(.075,9.95,.052),blue,.008)
    for y in [ty-4.7,ty-1.6,ty+1.7,ty+4.7]:box('Trailer upright stake',(x,y,1.43),(.105,.11,.72),trim,.008)
for y in [ty-4.85,ty+4.85]:box('Trailer end rail',(tx,y,1.0),(3.32,.13,.22),blue,.008)
for y in [ty-.8,ty+.6]:
    for x in [tx-1.5,tx+1.5]:
        # Standard wheel axis is Y; rotate the assembled X-axis wheel to align the trailer.
        before=set(b.current.objects);wheel('Trailer road wheel',0,0,.57,.56,.33)
        bpy.context.view_layer.update()
        from mathutils import Matrix
        transform=Matrix.Translation((x,y,0))@Matrix.Rotation(math.pi/2,4,'Z')
        for o in set(b.current.objects)-before:o.matrix_world=transform@o.matrix_world
pipe('Trailer drawbar',[(tx-.9,ty+4.8,.65),(tx,ty+6.2,.65),(tx+.9,ty+4.8,.65)],.075,trim)

# Six-wheel, faded Soviet-style fire appliance at the far end of the yard.
fx,fy=12.1,11.4
box('Fire engine ladder frame',(fx,fy,.77),(6.8,2.15,.30),trim,.04)
box('Fire engine water tank',(fx+1.05,fy,1.95),(4.1,2.25,1.86),red,.16)
box('Fire engine cab',(fx-1.64,fy,2.06),(1.72,2.26,2.0),red,.14)
box('Long engine bonnet',(fx-2.98,fy,1.65),(1.10,1.95,.85),red,.16)
box('Firetruck front radiator',(fx-3.55,fy,1.58),(.045,1.41,.6),black,.045)
for z in [1.33+i*.07 for i in range(8)]:box('Radiator grille horizontal slat',(fx-3.59,fy,z),(.025,1.42,.017),silver)
box('Fire truck front bumper',(fx-3.68,fy,.97),(.22,2.5,.20),silver,.03)
for yy in [fy-.86,fy+.86]:
    cyl('Round front headlight',(fx-3.54,yy,1.60),(fx-3.63,yy,1.60),.14,ivory,24)
    box('Cab side window',(fx-1.7,yy*0+fy+(-1.142 if yy<fy else 1.142),2.53),(1.1,.035,.68),glass,.055)
    box('Cab ivory door stripe',(fx-1.6,fy+(-1.153 if yy<fy else 1.153),1.89),(1.55,.022,.38),ivory,.005)
    box('Cab side door handle',(fx-1.1,fy+(-1.177 if yy<fy else 1.177),2.12),(.14,.035,.03),silver,.005)
    pipe('Truck mirror arm',[(fx-2.24,fy+(-1.14 if yy<fy else 1.14),2.57),(fx-2.34,fy+(-1.45 if yy<fy else 1.45),2.66)],.025,trim)
    box('Truck rearview mirror',(fx-2.34,fy+(-1.45 if yy<fy else 1.45),2.64),(.13,.08,.22),trim,.025)
box('Fire engine front windshield',(fx-2.52,fy,2.58),(.035,1.88,.65),glass,.04)
box('Windshield divider',(fx-2.55,fy,2.58),(.06,.04,.7),ivory,.005)
for xx in [fx-2.45,fx+.96,fx+2.45]:
    for yy in [fy-1.12,fy+1.12]:wheel('Fire engine road wheel',xx,yy,.67,.65,.36)
for yy in [fy-1.17,fy+1.17]:
    box('Tank long faded ivory stripe',(fx+1.03,yy,2.09),(3.98,.025,.30),ivory)
    for xx in [fx-.3,fx+.9,fx+2.1]:
        box('Equipment locker',(xx,yy*1.0,1.55),(1.05,.04,.8),red,.04)
        box('Locker latch',(xx,yy-.035,1.67),(.20,.04,.035),silver,.008)
    for z in [2.76,2.91]:pipe('Rooftop ladder longitudinal rail',[(fx-.4,yy*.0+fy-.72,z),(fx+2.9,fy-.72,z)],.022,trim)
for xx in [fx-.3+i*.28 for i in range(12)]:cyl('Roof ladder rung',(xx,fy-.82,2.89),(xx,fy+.65,2.89),.022,trim)
for yy in [fy-.67,fy+.67]:pipe('Rolled roof hose',[(fx-.1,yy,3.06),(fx+1.1,yy,3.06),(fx+2.5,yy,3.06)],.105,black)
for yy in [fy-.72,fy+.72]:cyl('Old blue beacon',(fx-1.6,yy,3.05),(fx-1.6,yy,3.24),.11,blue,24)
text('Fire engine faded fleet marking','01',(fx+.8,fy-1.205,2.36),.37,white)

def burnt_car(x,y):
    body=b.material('Burnt car peeling grey metal',(.14,.16,.15),rough=.8,metal=.5,scale=2,bump=.016)
    box('Burned sedan lower body',(x,y,.59),(3.9,1.72,.5),body,.20)
    box('Burned sedan hood',(x-1.34,y,.95),(1.19,1.61,.20),body,.09)
    verts=[(-.9,-.75,.82),(-.9,.75,.82),(.95,.75,.82),(.95,-.75,.82),(-.43,-.62,1.54),(-.43,.62,1.54),(.65,.62,1.54),(.65,-.62,1.54)]
    b.mesh('Burned sedan cabin shell',verts,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],glass,(x,y,0))
    box('Sedan rusted roof',(x+.1,y,1.56),(1.16,1.3,.055),body,.04)
    for yy in [y-.79,y+.79]:
        pipe('Sedan window frame',[(x-.88,yy,.85),(x-.43,yy*.0+y+(-.62 if yy<y else .62),1.53),(x+.64,y+(-.62 if yy<y else .62),1.53),(x+.95,yy,.85)],.035,body)
        cyl('Sedan centre window pillar',(x+.18,yy,.84),(x+.18,y+(-.63 if yy<y else .63),1.53),.035,body)
    for xx in [x-1.23,x+1.25]:
        for yy in [y-.83,y+.83]:wheel('Burnt sedan wheel',xx,yy,.4,.38,.23)
    for i in range(9):rock('Charred car surface blister',(x+random.uniform(-1.6,1.6),y-.88,random.uniform(.55,.95)),(.15,.025,.10),black,.2)
burnt_car(8.8,5.3)
box('Background delivery truck cargo box',(9.2,18,2),(4.5,2.2,2.55),tan,.05)
box('Background delivery truck cab',(6.1,18,1.76),(1.72,2.18,2.35),wood,.11)
box('Delivery truck windscreen',(5.21,18,2.30),(.04,1.85,.62),glass,.03)
for xx in [6.1,10.25]:
    for yy in [16.94,19.06]:wheel('Background truck wheel',xx,yy,.57,.54,.3)

# Drums, crates, refuse and construction debris.
b.group('Yard clutter')
def barrel(x,y,z=0,mat=rust):
    cyl('Steel drum shell',(x,y,z+.05),(x,y,z+.98),.38,mat,24)
    for zz in [.08,.34,.69,.95]:cyl('Drum rolled reinforcing hoop',(x,y,z+zz-.019),(x,y,z+zz+.019),.398,trim,24)
    cyl('Dusty drum lid',(x,y,z+.98),(x,y,z+1.00),.365,wood,24)
    cyl('Drum filling bung',(x+.13,y,z+1),(x+.13,y,z+1.015),.045,trim,12)
def crate(x,y,z,w=.72):
    box('Wooden shipping crate',(x,y,z+w/2),(w,w*.82,w),wood,.015)
    for zz in [z+.06,z+w-.06]:box('Crate front batten',(x,y-w*.42,zz),(w+.04,.065,.07),silver,.003)
    for xx in [x-w*.42,x+w*.42]:box('Crate upright batten',(xx,y-w*.42,z+w/2),(.06,.065,w),silver,.003)
def carton(x,y,z=0,w=.65):
    box('Cardboard packing box',(x,y,z+w*.4),(w,w*.78,w*.8),card,.025)
    box('Box packing tape',(x,y,z+w*.805),(.07,w*.79,.007),wood)
    for k in range(3):box('Faded box shipping label',(x-w*.23+k*.09,y-w*.40,z+w*.43),(.045,.012,.07),rust)
for x,y in [(7.3,-1.9),(7.6,-.8),(7.45,.2),(6.6,1.8),(5.8,1.9),(3,1.2)]:barrel(x,y)
for x,y,z in [(7.7,-2.8,0),(8.2,-2.3,0),(7.7,-2.8,.62),(8.4,-3,0),(-10,-7.1,0),(-10.8,-7.4,0),(-10.5,-7.2,.7)]:carton(x,y,z)
for x,y,z in [(12.4,2.0,0),(13.1,2.8,0),(12.5,2.1,.72),(10.8,3.3,0)]:crate(x,y,z,.85)
for x,y in [(13.8,.4),(14.8,1.4),(14.4,-.7),(13.2,-1.7)]:carton(x,y,0,.86)
for x,y in [(-6.8,-3.0),(-6,-3.1),(-7.6,-3.1),(-7,-3.5),(-5.7,-2.9),(10.9,9.5),(16,9.1),(16.8,10.2)]:
    rock('Black rubbish sack',(x,y,.36),(.55,.45,.42),black,.23,True)
    cyl('Tied refuse bag neck',(x,y,.63),(x+.04,y,.82),.065,black)
for i in range(175):
    x=random.uniform(-11,17);y=random.uniform(-15,16)
    if -9<x<9 and 5.7<y<12.5:continue
    r=random.uniform(.025,.12);rock('Loose plaster and road rubble',(x,y,.015),(r,r*.7,r*.4),concrete,.28)
for i in range(45):
    x=random.uniform(-11,15);y=random.uniform(-13,9)
    w=random.uniform(.07,.22);h=random.uniform(.10,.3)
    o=b.mesh('Windblown folded paper',[(-w,-h,0),(w,-h,.02),(w,h,.005),(-w,h,.045),(0,0,.055)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],paper,(x,y,.005));o.rotation_euler[2]=random.random()*math.tau
for x,y in [(4,-6.7),(1.4,-4.1),(9,-3.4),(-1,-8.4),(15,-13)]:
    verts=[];faces=[]
    for i in range(9):
        for j in range(6):verts.append((i*.12,j*.12,.035+.075*math.sin(i*2.1+j)*math.sin(j*1.4)))
    for i in range(8):
        for j in range(5):k=i*6+j;faces.append((k,k+6,k+7,k+1))
    o=b.mesh('Crumpled discarded fabric',verts,faces,cloth,(x,y,.02));o.rotation_euler[2]=random.random()*6
for i in range(24):
    x=random.uniform(-10,15);y=random.uniform(-8,13)
    o=box('Broken timber splinter',(x,y,.025),(random.uniform(.25,.9),.035,.027),wood,.003);o.rotation_euler[2]=random.random()*6.28

# Enclosing urban apartment blocks with repeated windows and inset balconies.
b.group('Surrounding apartment blocks')
def apartment(name,cx,cy,width,height,rows,cols):
    box(name+' main stucco volume',(cx,cy,height/2),(width,5,height),wall)
    box(name+' roof cornice',(cx,cy,height),(width+.5,5.4,.25),balcony)
    step=width/cols;rise=(height-1.4)/rows
    for row in range(rows):
        z=1.6+row*rise
        for col in range(cols):
            x=cx-width/2+(col+.5)*step
            pane=glass if (row+col)%5 else tan
            box(name+' shadowed window',(x,cy-2.54,z),(step*.67,.06,rise*.62),pane)
            for xx in [x-step*.34,x,x+step*.34]:box(name+' pale window mullion',(xx,cy-2.61,z),(.047,.07,rise*.66),balcony)
            for zz in [z-rise*.32,z+rise*.32]:box(name+' pale window lintel',(x,cy-2.61,zz),(step*.72,.12,.07),balcony)
            if col%4 in [1,2]:
                box(name+' enclosed balcony parapet',(x,cy-2.72,z-rise*.33),(step*.93,.35,.46),balcony)
                box(name+' balcony floor edge',(x,cy-2.72,z-rise*.5),(step*.98,.42,.10),balcony)
        box(name+' horizontal floor joint',(cx,cy-2.55,z-rise*.5),(width,.025,.028),mortar)
    for col in range(cols+1):box(name+' facade pilaster',(cx-width/2+col*step,cy-2.57,height/2),(.10,.16,height),balcony)
apartment('Long background residential block',8,29,58,20.5,8,27)
apartment('Rear left apartment building',-17,24,23,17,6,11)
box('Massive left concrete tower',(-23,11,15),(9,12,30),wall)
for z in range(2,30,2):box('Tower horizontal construction joint',(-18.45,11,z),(.08,12,.045),balcony)
for x in [-27,-24,-21]:box('Tower vertical construction joint',(x,4.95,15),(.05,.045,30),balcony)
for x in [-15,-4,7,16,25]:box('Distant roof chimney',(x,29,21.2),(.6,.9,1.4),wall)
cyl('Distant pointed roof spire',(-11,31,20),(-11,31,24),.75,wall,8,r2=0)
b.group('Trees and street furniture')
for x,y in [(-15,16),(-18,12),(3,24),(18,22),(23,23),(-7,23)]:
    cyl('Street tree trunk',(x,y,0),(x,y,5.5),.13,wood)
    for j in range(28):
        a=random.uniform(0,math.tau);r=random.uniform(0,1.7);z=random.uniform(3.6,6.8)
        rock('Olive foliage cluster',(x+math.cos(a)*r,y+math.sin(a)*r,z),(.7,.6,.65),leaf,.28)
for x,y in [(-10,12),(9.5,15),(20,17)]:
    pipe('Bent street lamp pole',[(x,y,0),(x,y,8.1),(x-.3,y,8.4),(x-1.7,y,8.5)],.055,trim)
    box('Street light head',(x-1.8,y,8.45),(.66,.23,.13),silver,.07)

# Hazy, backlit daylight and a high three-quarter viewpoint.
b.group('Lighting and camera')
world=bpy.data.worlds.new('R1 | Pale overcast urban sky');world.use_nodes=True;scene.world=world
n=world.node_tree.nodes;l=world.node_tree.links;sky=n.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_elevation=math.radians(27);sky.sun_rotation=math.radians(135);sky.sun_disc=False;sky.altitude=.1;sky.air_density=1.8;sky.aerosol_density=3
l.new(sky.outputs['Color'],n['Background'].inputs['Color']);n['Background'].inputs['Strength'].default_value=.45
sun=b.light('Low warm sun','SUN',(-15,12,25),2.0,(1,.91,.76),target=(0,0,0));sun.data.angle=.12
b.light('Broad courtyard sky fill','AREA',(5,-5,20),1700,(.77,.85,1),18,(0,5,0))
fog=bpy.data.materials.new('R1 | Fine sunlit atmospheric dust');fog.use_nodes=True;nodes=fog.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');sc=nodes.new('ShaderNodeVolumeScatter');sc.inputs['Color'].default_value=(.77,.78,.73,1);sc.inputs['Density'].default_value=.003;sc.inputs['Anisotropy'].default_value=.25;fog.node_tree.links.new(sc.outputs[0],out.inputs['Volume'])
o=box('Atmospheric haze volume',(0,10,12),(110,130,28),None);o.data=o.data.copy();o.data.materials.append(fog);o.display_type='WIRE'
data=bpy.data.cameras.new('Ref 1 still camera');cam=bpy.data.objects.new('R1 | Ref 1 still camera',data);b.current.objects.link(cam);cam.location=(13,-21,11);cam.rotation_euler=(Vector((0,6,2.3))-cam.location).to_track_quat('-Z','Y').to_euler();data.lens=29;data.sensor_width=36;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=96;scene.cycles.use_denoising=True;scene.cycles.max_bounces=8;scene.cycles.volume_bounces=1
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='OPTIX'
scene.cycles.device='GPU';scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=50;scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/'preview.png')
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.7
scene['reference']='ref-1.jpg';scene['description']='Hazy abandoned service courtyard with prefab workshops, blue rubble skip, fire engine, burnt sedan and flatbed trailer.'
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ref-1-reconstruction.blend'))
result={'scene':scene.name,'objects':len(scene.objects),'file':bpy.data.filepath}
