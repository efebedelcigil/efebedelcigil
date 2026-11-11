"""Render reusable physical through-hole parts with the board's orthographic camera.

Run with Blender in background mode. Normal profile refreshes reuse these assets.
"""
import bpy,math,json
from pathlib import Path
from mathutils import Vector,Matrix
import numpy as np
from bpy_extras.object_utils import world_to_camera_view

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/components3d';OUT.mkdir(exist_ok=True)
M=np.array([[1,-.24],[.055,.88]]);singular=np.linalg.svd(M)[1][0]
r=Vector((M[0,0]/singular,-M[0,1]/singular,0));r.z=-math.sqrt(1-r.length_squared)
u=Vector((-M[1,0]/singular,M[1,1]/singular,0));u.z=-(r.x*u.x+r.y*u.y)/r.z
w=r.cross(u).normalized();rotation=Matrix(((r.x,u.x,w.x),(r.y,u.y,w.y),(r.z,u.z,w.z)))
RES=384;ORTHO=36

def material(name,color,metal=0,rough=.35):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 return m

silver=material('Tinned metal',(.48,.55,.56),.85,.24)
solder=material('Solder fillets',(.43,.49,.48),.82,.23)
copper=material('Copper winding',(.63,.27,.075),.82,.25)
tan=material('Resistor ceramic',(.53,.39,.22),0,.35)
black=material('Moulded package',(.023,.032,.038),.05,.38)
blue=material('Capacitor sleeve',(.026,.12,.21),.22,.3)
stripe=material('Sleeve polarity stripe',(.52,.59,.58),.3,.34)
core=material('Ferrite toroid',(.07,.085,.075),.1,.52)
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
 return finish(o,mat,bevel)

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
 scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.5,.55,.6,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.6;scene.view_settings.view_transform='AgX'
 camera=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));bpy.context.collection.objects.link(camera);camera.location=w*65;camera.rotation_euler=rotation.to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=ORTHO;scene.camera=camera
 for loc,power,size in [((-12,-14,28),12500,16),((14,5,20),9000,13),((-4,15,12),5000,10)]:
  light=bpy.data.objects.new('Softbox',bpy.data.lights.new('Softbox','AREA'));bpy.context.collection.objects.link(light);light.location=loc;light.rotation_euler=(-light.location).to_track_quat('-Z','Y').to_euler();light.data.energy=power;light.data.shape='DISK';light.data.size=size
 return scene

metadata={'projection':M.flatten().tolist(),'units_per_pixel':float(singular*ORTHO/RES),'resolution':RES,'parts':{}}
for level in range(1,5):
 scene=setup();contacts=[]
 if level==1:
  contacts=[(-8,0),(8,0)]
  cylinder('Axial resistor body',(0,0,3),2,12,tan,(1,0,0))
  for x,mat in [(-3.7,bands[0]),(-1.5,bands[1]),(3.7,bands[2])]:cylinder('Resistor band',(x,0,3),2.035,.85,mat,(1,0,0))
  for sign in [-1,1]:wire('Bent axial lead',[(sign*8,0,.4),(sign*8,0,2),(sign*7.8,0,3),(sign*6,0,3)],.28,silver)
 elif level==2:
  contacts=[(-3,0),(3,0)]
  cylinder('Electrolytic sleeve',(0,0,9),5.1,15,blue)
  cylinder('Aluminium top',(0,0,16.55),4.7,.35,silver)
  cylinder('Lower seal',(0,0,1.35),4.7,.7,black)
  for xx in [-1,1]:wire('Pressure vent',[(xx*-2.5,-2.5,16.77),(xx*2.5,2.5,16.77)],.08,black)
  # A real curved sleeve stripe, rather than a flat icon on the top.
  for a in np.linspace(-.2,.2,8):wire('Polarity stripe',[(5.14*math.cos(a),5.14*math.sin(a),z) for z in [2,16]],.15,stripe)
  for x,y in contacts:wire('Capacitor lead',[(x,y,.3),(x,y,1.6)],.3,silver)
 elif level==3:
  contacts=[(-7.6,0),(7.6,0)]
  bpy.ops.mesh.primitive_torus_add(major_radius=4.5,minor_radius=2.2,major_segments=64,minor_segments=20,location=(0,0,3.5));finish(bpy.context.object,core)
  points=[]
  for i in range(1100):
   theta=i/(1100-1)*2*math.pi*12;phi=i/(1100-1)*2*math.pi
   radius=4.5+2.36*math.cos(theta);points.append((radius*math.cos(phi),radius*math.sin(phi),3.5+2.36*math.sin(theta)))
  wire('Continuous toroidal winding',points,.42,copper)
  for sign in [-1,1]:wire('Inductor lead',[(sign*7.6,0,.3),(sign*7,0,2),(sign*6.5,0,3.5)],.35,silver)
 else:
  contacts=[(side*7.6,y) for side in [-1,1] for y in [-6,-2,2,6]]
  box('Raised DIP moulding',(0,0,3.4),(11.5,18,4.3),black,.55)
  for x,y in contacts:wire('Formed DIP leg',[(x,y,.3),(x,y,1.1),(math.copysign(7,x),y,2.6),(math.copysign(5.75,x),y,2.6)],.36,silver)
  cylinder('Pin one recess',(-3.5,-6.4,5.57),.48,.08,stripe)
  for y,length in [(-1,5),(1,3.8),(3,4.5)]:box('Laser-etched marking',(0,y,5.57),(length,.24,.025),stripe,.03)
 for x,y in contacts:pad(x,y)
 scene.render.filepath=str(OUT/f'part-{level}.png');bpy.ops.render.render(write_still=True)
 # Contact coordinates are on the board plane; world Y is negative board Y.
 metadata['parts'][str(level)]={'contacts':[[x,-y] for x,y in contacts]}
(OUT/'render-metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
