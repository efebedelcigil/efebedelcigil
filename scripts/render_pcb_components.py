"""Render reusable physical through-hole parts with the board's orthographic camera.

Run with Blender in background mode. Normal profile refreshes reuse these assets.
"""
import bpy,math,json,os
from pathlib import Path
from mathutils import Vector,Matrix
import numpy as np
from bpy_extras.object_utils import world_to_camera_view

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/components3d';OUT.mkdir(exist_ok=True)
M=np.array([[1,-.10],[.045,.72]]);singular=np.linalg.svd(M)[1][0]
r=Vector((M[0,0]/singular,-M[0,1]/singular,0));r.z=-math.sqrt(1-r.length_squared)
u=Vector((-M[1,0]/singular,M[1,1]/singular,0));u.z=-(r.x*u.x+r.y*u.y)/r.z
w=r.cross(u).normalized();rotation=Matrix(((r.x,u.x,w.x),(r.y,u.y,w.y),(r.z,u.z,w.z)))
RES=640;ORTHO=64

def material(name,color,metal=0,rough=.35):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if name in ['Moulded package','Ferrite toroid']:p.inputs['Specular IOR Level'].default_value=.3
 return m

silver=material('Tinned metal',(.36,.43,.49),.5,.5)
solder=material('Solder fillets',(.39,.49,.52),.45,.38)
copper=material('Copper winding',(.63,.27,.075),.82,.25)
tan=material('Resistor ceramic',(.53,.39,.22),0,.35)
black=material('Moulded package',(.009,.017,.026),0,.56)
blue=material('Capacitor sleeve',(.014,.105,.32),.08,.34)
stripe=material('Sleeve polarity stripe',(.52,.59,.58),.3,.34)
core=material('Ferrite toroid',(.025,.037,.045),0,.58)
bands=[material('Band brown',(.14,.055,.025)),material('Band black',(.012,.016,.018)),material('Band gold',(.55,.33,.075),.65)]

def finish(obj,mat,bevel=0):
 obj.data.materials.append(mat)
 if bevel:
  mod=obj.modifiers.new('Edge radii','BEVEL');mod.width=bevel;mod.segments=3
 if obj.type=='MESH':
  for f in obj.data.polygons:f.use_smooth=True
 return obj

def cylinder(name,loc,radius,depth,mat,axis=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=radius,depth=depth,location=loc);obj=bpy.context.object;obj.name=name
 if axis:obj.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
 return finish(obj,mat,.08)

def box(name,loc,size,mat,bevel=.15):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 finish(o,mat,bevel)
 mod=o.modifiers.new('Stable face normals','WEIGHTED_NORMAL');mod.keep_sharp=True
 return o

def wire(name,points,radius,mat):
 curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D';curve.bevel_depth=radius;curve.bevel_resolution=3
 line=curve.splines.new('POLY');line.points.add(len(points)-1)
 for point,coords in zip(line.points,points):point.co=(*coords,1)
 obj=bpy.data.objects.new(name,curve);bpy.context.collection.objects.link(obj);obj.data.materials.append(mat)
 return obj

def lathe(name,xy,profile,mat):
 vertices=[];faces=[];n=40
 for radius,z in profile:
  vertices.extend((xy[0]+radius*math.cos(i*2*math.pi/n),xy[1]+radius*math.sin(i*2*math.pi/n),z) for i in range(n))
 for j in range(len(profile)-1):
  for i in range(n):faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);return finish(o,mat)

def pad(x,y):
 lathe('Annular pad',(x,y),[(.38,.02),(1.35,.02),(1.35,.13),(.38,.13)],silver)
 lathe('Concave solder meniscus',(x,y),[(1.12,.14),(.86,.22),(.61,.4),(.43,.72),(.32,.91)],solder)

def setup():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
 scene.render.resolution_x=RES;scene.render.resolution_y=RES;scene.render.resolution_percentage=100;scene.render.film_transparent=True
 scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
 scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.5,.55,.6,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35;scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
 shade=scene.display.shading;shade.light='STUDIO';shade.color_type='MATERIAL';shade.show_shadows=True;shade.shadow_intensity=.25;shade.show_cavity=True;shade.cavity_type='BOTH';shade.cavity_ridge_factor=.55;shade.cavity_valley_factor=.7;shade.show_specular_highlight=False;shade.show_object_outline=False
 camera=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));bpy.context.collection.objects.link(camera);camera.location=w*65;camera.rotation_euler=rotation.to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=ORTHO;scene.camera=camera
 for loc,power,size in [((-12,-14,28),5000,16),((14,5,20),1800,13),((-4,15,12),2600,9)]:
  light=bpy.data.objects.new('Softbox',bpy.data.lights.new('Softbox','AREA'));bpy.context.collection.objects.link(light);light.location=loc;light.rotation_euler=(-light.location).to_track_quat('-Z','Y').to_euler();light.data.energy=power;light.data.shape='DISK';light.data.size=size
 return scene

metadata={'projection':M.flatten().tolist(),'units_per_pixel':float(singular*ORTHO/RES),'resolution':RES,'parts':{}}
selected=os.environ.get('PCB_PART_VARIANTS')
if selected:metadata=json.loads((OUT/'render-metadata.json').read_text(encoding='utf-8'))
for variant in ([int(v) for v in selected.split(',')] if selected else range(1,9)):
 level=(variant-1)%4+1
 scene=setup();contacts=[]
 if level==1:
  contacts=[(-8.8,0),(8.8,0)]
  box('SMD power resistor',(0,0,2.6),(17.5,11.2,3.8),black,.35)
  for x in [-8.1,8.1]:box('Tinned end cap',(x,0,2.6),(1.6,11.3,3.9),silver,.15)
  for x in [-1.8,0,1.8]:box('Laser resistance marking',(x,0,4.85),(.5,2.2,.04),stripe,.04)
 elif level==2:
  contacts=[(-4.1,0),(4.1,0)]
  cylinder('Electrolytic sleeve',(0,0,10),8.3,17,blue)
  cylinder('Aluminium top',(0,0,18.55),7.7,.35,silver)
  cylinder('Black rim',(0,0,18.25),8.4,.35,black)
  cylinder('Lower seal',(0,0,1.35),7.85,.7,black)
  for xx in [-1,1]:wire('Pressure vent',[(xx*-3.2,-3.2,18.77),(xx*3.2,3.2,18.77)],.22,black)
  # A real curved sleeve stripe, rather than a flat icon on the top.
  vertices=[(8.34*math.cos(a),8.34*math.sin(a),z) for z in [2,18] for a in np.linspace(-1.7,-1.12,16)]
  mesh=bpy.data.meshes.new('Printed polarity band');mesh.from_pydata(vertices,[],[(i,i+1,i+17,i+16) for i in range(15)]);mesh.update()
  band=bpy.data.objects.new('Printed polarity band',mesh);bpy.context.collection.objects.link(band);finish(band,stripe)
  for x,y in contacts:wire('Capacitor lead',[(x,y,.3),(x,y,1.6)],.3,silver)
 elif level==3:
  contacts=[(-7.7,0),(7.7,0)]
  cylinder('SMD ferrite bottom',(0,0,1.3),7.5,1.8,core)
  cylinder('Ferrite centre',(0,0,4.5),3.8,6.5,core)
  cylinder('Ferrite top',(0,0,8),7.4,1.2,core)
  points=[]
  for i in range(750):
   theta=i/(750-1)*2*math.pi*8;z=2+i/(750-1)*5
   points.append((5.5*math.cos(theta),5.5*math.sin(theta),z))
  wire('Exposed side winding',points,.4,copper)
 else:
  contacts=[(side*8.2,y) for side in [-1,1] for y in [-6,-2,2,6]]
  box('Raised SOIC moulding',(0,0,3.7),(16,17,5.6),black,.55)
  for x,y in contacts:wire('Short SOIC lead',[(x,y,.3),(x,y,1.2),(math.copysign(7.5,x),y,2),(math.copysign(7,x),y,2)],.34,silver)
  cylinder('Pin one recess',(-4,-6,6.56),.48,.07,stripe)
  for y,length in [(-1,5),(1,3.8),(3,4.5)]:box('Laser-etched marking',(0,y,6.56),(length,.24,.025),stripe,.03)

 for x,y in contacts:
  if level in [1,3,4]:
   box('SMD plated landing',(x,y,.1),(2.6,2.2 if level==4 else 5.8,.18),silver,.12)
   for xx in [x-.6,x+.6]:cylinder('Solder toe',(xx,y,.35),.5,1.8 if level==4 else 5.2,solder,(0,1,0))
  else:pad(x,y)

 factor={1:1.1,2:1.0,3:1.2,4:1.1}[level]
 for obj in list(scene.objects):
  if obj.type in ['MESH','CURVE']:obj.matrix_world=Matrix.Diagonal((1,1,factor,1)) @ obj.matrix_world

 if variant>4:
  for obj in list(scene.objects):
   if obj.type in ['MESH','CURVE']:obj.matrix_world=Matrix.Rotation(math.pi/2,4,'Z') @ obj.matrix_world
  contacts=[(-y,x) for x,y in contacts]
 colors={'Moulded package':(.014,.035,.07),'Capacitor sleeve':(.018,.20,.48),'Ferrite toroid':(.045,.075,.11),'Tinned metal':(.54,.68,.74),'Solder fillets':(.45,.57,.62)}
 for mat in bpy.data.materials:
  if mat.name in colors:
   mat.diffuse_color=(*colors[mat.name],1);mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*colors[mat.name],1)
 scene.render.filepath=str(OUT/f'part-{variant}.png');bpy.ops.render.render(write_still=True)
 # Contact coordinates are on the board plane; world Y is negative board Y.
 metadata['parts'][str(variant)]={'contacts':[[x,-y] for x,y in contacts]}
 bpy.context.view_layer.update()
 exclude=('SMD plated landing','Solder toe','Annular pad','Concave solder','Bent axial lead','Capacitor lead','Formed DIP leg','Short SOIC lead')
 body=[o for o in scene.objects if o.type in ['MESH','CURVE'] and not o.name.startswith(exclude)]
 pts=[o.matrix_world@Vector(v) for o in body for v in o.bound_box]
 bounds=[min(r.dot(v) for v in pts)*singular,-max(u.dot(v) for v in pts)*singular,max(r.dot(v) for v in pts)*singular,-min(u.dot(v) for v in pts)*singular]
 metadata['parts'][str(variant)]['body_plane_bounds']=[min(v.x for v in pts),-max(v.y for v in pts),max(v.x for v in pts),-min(v.y for v in pts)]
 metadata['parts'][str(variant)]['body_screen_bounds']=bounds
 metadata['parts'][str(variant)]['body_screen_center']=[(bounds[0]+bounds[2])/2,(bounds[1]+bounds[3])/2]
(OUT/'render-metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
