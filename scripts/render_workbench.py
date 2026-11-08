import argparse
import math
import json
from pathlib import Path

import bpy
from mathutils import Vector


def arguments():
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    parser.add_argument('--theme', choices=['light', 'dark'], default='dark')
    parser.add_argument('--frame', type=int)
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=180)
    parser.add_argument('--width', type=int, default=1120)
    parser.add_argument('--samples', type=int, default=32)
    parser.add_argument('--mobile', action='store_true')
    parser.add_argument('--activity')
    return parser.parse_args(sys.argv[sys.argv.index('--') + 1:])


args = arguments()
out = Path(args.out)
if not out.is_absolute():
    out = Path(__file__).resolve().parents[1] / out
out.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.film_transparent = True
scene.render.resolution_x = args.width
scene.render.resolution_y = round(args.width * (0.92 if args.mobile else 0.4))
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.fps = 15
scene.frame_start = 1
scene.frame_end = 180
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs[0].default_value = (0.42, 0.49, 0.58, 1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value = 0.45
scene.view_settings.view_transform = 'AgX'
if hasattr(scene, 'eevee') and hasattr(scene.eevee, 'taa_render_samples'):
    scene.eevee.taa_render_samples = args.samples


def material(name, color, metal=0, roughness=0.4, emission=0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Metallic'].default_value = metal
    bsdf.inputs['Roughness'].default_value = roughness
    if emission:
        bsdf.inputs['Emission Color'].default_value = (*color, 1)
        bsdf.inputs['Emission Strength'].default_value = emission
    return mat


silver = material('Satin aluminium', (0.63, 0.72, 0.78), 0.7, 0.28)
edge = material('Machined edges', (0.83, 0.87, 0.9), 0.72, 0.23)
navy = material('Graphite joints', (0.035, 0.059, 0.088), 0.38, 0.34)
teal = material('Teal enamel', (0.025, 0.47, 0.39), 0.35, 0.32)
amber = material('Amber dial', (0.91, 0.35, 0.13), 0.28, 0.36)
gold = material('Copper pads', (0.62, 0.39, 0.13), 0.72, 0.3)
boardmat = material('PCB solder mask', (0.025, 0.19, 0.145), 0.3, 0.44)
activity_materials = [material('Activity '+str(i), color, 0.3, 0.4) for i,color in enumerate([
    (.07,.16,.15),(.04,.30,.22),(.03,.46,.30),(.08,.62,.40),(.25,.78,.54)
])]
activity_path = Path(args.activity) if args.activity else Path(__file__).resolve().parents[1]/'assets/workbench-data.json'
activity = json.loads(activity_path.read_text(encoding='utf-8')) if activity_path.exists() else None
trace = material('Screen trace', (0.15, 0.85, 0.65), 0, 0.4, 1.2)
scanmat = bpy.data.materials.new('Inspection overlay')
scanmat.use_nodes = True
scanmat.surface_render_method = 'DITHERED'
nodes=scanmat.node_tree.nodes
nodes.clear()
transparent=nodes.new('ShaderNodeBsdfTransparent')
emission=nodes.new('ShaderNodeEmission')
emission.inputs['Color'].default_value=(.15,.85,.65,1)
fade=nodes.new('ShaderNodeMixShader')
output=nodes.new('ShaderNodeOutputMaterial')
scanmat.node_tree.links.new(transparent.outputs[0],fade.inputs[1])
scanmat.node_tree.links.new(emission.outputs[0],fade.inputs[2])
scanmat.node_tree.links.new(fade.outputs[0],output.inputs['Surface'])
screenmat = material('Screen', (0.012, 0.027, 0.041), 0.1, 0.36)
gridmat = material('Screen grid', (0.12, 0.21, 0.24), 0, 0.5, 0.3)
ink = material('Name', (0.84, 0.89, 0.93) if args.theme == 'dark' else (0.045, 0.07, 0.11), 0, 1, 1)
muted = material('Subtitle', (0.42, 0.56, 0.62) if args.theme == 'dark' else (0.16, 0.30, 0.35), 0, 1, 1)
if args.theme == 'light':
    for mat,color in [(ink,(.006,.014,.022)),(muted,(.018,.05,.065))]:
        nodes=mat.node_tree.nodes
        nodes.clear()
        surface=nodes.new('ShaderNodeEmission')
        surface.inputs['Color'].default_value=(*color,1)
        output=nodes.new('ShaderNodeOutputMaterial')
        mat.node_tree.links.new(surface.outputs['Emission'],output.inputs['Surface'])


def empty(name, loc=(0, 0, 0), parent=None):
    obj = bpy.data.objects.new(name, None)
    scene.collection.objects.link(obj)
    obj.parent = parent
    obj.location = loc
    return obj


assembly = empty('Workbench')


def finish(obj, name, mat, parent):
    obj.name = name
    obj.data.materials.append(mat)
    obj.parent = parent
    return obj


def box(name, loc, scale, mat, parent=assembly, bevel=0.035):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    obj = bpy.context.object
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.location = loc
    finish(obj, name, mat, parent)
    if bevel:
        mod = obj.modifiers.new('Edge radius', 'BEVEL')
        mod.width = bevel
        mod.segments = 3
        obj.modifiers.new('Face normals', 'WEIGHTED_NORMAL')
    return obj


def cylinder(name, loc, radius, depth, mat, parent=assembly):
    bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=radius, depth=depth)
    obj = bpy.context.object
    obj.location = loc
    finish(obj, name, mat, parent)
    mod = obj.modifiers.new('Machined rim', 'BEVEL')
    mod.width = min(0.018, depth / 5)
    mod.segments = 3
    obj.modifiers.new('Face normals', 'WEIGHTED_NORMAL')
    for face in obj.data.polygons:
        face.use_smooth = len(face.vertices) == 4
    return obj


def line(name, points, mat, radius=0.008, parent=assembly):
    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '3D'
    curve.bevel_depth = radius
    curve.bevel_resolution = 2
    spline = curve.splines.new('POLY')
    spline.points.add(len(points) - 1)
    for p, v in zip(spline.points, points):
        p.co = (*v, 1)
    obj = bpy.data.objects.new(name, curve)
    scene.collection.objects.link(obj)
    obj.parent = parent
    obj.data.materials.append(mat)
    return obj


def text(name, body, loc, size, mat, parent=assembly):
    curve = bpy.data.curves.new(name, 'FONT')
    curve.body = body
    curve.size = size
    curve.extrude = 0.001
    curve.resolution_u = 8
    font = Path('C:/Windows/Fonts/trebuc.ttf')
    if font.exists():
        curve.font = bpy.data.fonts.load(str(font), check_existing=True)
    obj = bpy.data.objects.new(name, curve)
    scene.collection.objects.link(obj)
    obj.parent = parent
    obj.location = loc
    curve.materials.append(mat)
    return obj


base = (-0.9, 0.35)
box('Base plate', (*base, 0.1), (0.72, 0.66, 0.18), edge)
cylinder('Base housing', (*base, 0.36), 0.26, 0.4, navy)
cylinder('Base accent', (*base, 0.56), 0.265, 0.06, teal)
cylinder('Shoulder casing', (*base, 0.77), 0.22, 0.36, silver)
for x in [-0.25, 0.25]:
    for y in [-0.22, 0.22]:
        cylinder('Base bolt', (base[0]+x, base[1]+y, 0.2), 0.035, 0.014, navy)

l1, l2 = 0.95, 0.85
upper = empty('Shoulder', (*base, 0.98), assembly)
box('Upper link', (l1/2, 0, 0), (l1, 0.24, 0.16), silver, upper)
box('Upper inlay', (l1/2, 0, 0.083), (l1*0.57, 0.08, 0.009), navy, upper, 0.015)
cylinder('Shoulder lid', (0, 0, 0.08), 0.17, 0.07, navy, upper)
cylinder('Shoulder ring', (0, 0, 0.125), 0.13, 0.025, teal, upper)
lower = empty('Elbow', (l1, 0, -0.12), upper)
cylinder('Elbow housing', (0, 0, 0.06), 0.16, 0.28, navy, lower)
cylinder('Elbow encoder', (0, 0, 0.215), 0.115, 0.035, teal, lower)
box('Forearm', (l2/2, 0, 0), (l2, 0.19, 0.13), edge, lower)
box('Forearm inlay', (l2/2, 0, 0.07), (l2*.56, 0.06, 0.012), teal, lower, 0.014)
wrist = empty('Wrist', (l2, 0, 0), lower)
cylinder('Wrist housing', (0, 0, -0.02), 0.12, 0.25, navy, wrist)
inspection = empty('Inspection camera', (0, 0, .04), wrist)
box('Camera enclosure', (0,-.14,0), (.16,.13,.11), navy, inspection, .018)
lens = cylinder('Camera lens', (0,-.22,0), .045, .035, edge, inspection)
lens.rotation_euler.x = math.pi/2
glass = cylinder('Lens glass', (0,-.24,0), .032, .012, screenmat, inspection)
glass.rotation_euler.x = math.pi/2
slide = empty('Vertical slide', (0, 0, -0.15), wrist)
cylinder('Linear axis', (0, 0, -0.12), 0.055, 0.4, silver, slide)
box('Gripper body', (0, 0, -0.31), (0.23, 0.17, 0.12), navy, slide)
finger_a = box('Left jaw', (-0.085, 0, -0.41), (0.045, 0.11, 0.17), silver, slide, 0.012)
finger_b = box('Right jaw', (0.085, 0, -0.41), (0.045, 0.11, 0.17), silver, slide, 0.012)

box('PCB', (0.43, -0.61, 0.13), (1.1, 0.72, 0.07), boardmat)
for row in range(4):
    for col in range(7):
        x, y = 0.0+col*.13, -0.86+row*.15
        padmat = activity_materials[activity['days'][row*7+col]['level']] if activity else teal
        box('Activity pad', (x, y, 0.171), (.085, .09, .006), padmat, bevel=.006)
        if col < 6:
            line('PCB trace', [(x, y, .177),(x+.13,y,.177)], gold, .003)
for x,y in [(-.04,-.9),(.9,-.9),(-.04,-.32),(.9,-.32)]:
    cylinder('Board mount', (x,y,.18), .025, .025, edge)

knob = empty('Tuning dial', (-0.1, 0.06, .16), assembly)
cylinder('Dial plate', (0,0,-.04), .18, .09, navy, knob)
cylinder('Dial', (0,0,.03), .13, .12, amber, knob)
line('Dial marker', [(0,0,.097),(.09,0,.097)], edge, .01, knob)

plaque = empty('Name tile', (-.48,-1.07,.13), assembly)
box('Signature tile', (0,0,0), (.48,.31,.08), edge, plaque)
text('Initials','EVB',(-.17,-.07,.045),.17,navy,plaque)

tray = (-1.02,-.6,.18)
box('Parts tray', tray, (.43,.4,.07), silver)
chip = box('Component', (tray[0],tray[1],.25), (.14,.14,.09), navy, bevel=.012)
for i in range(3):
    box('Spare component', (tray[0]-.12+i*.12,tray[1]+.13,.25), (.075,.07,.06), teal, bevel=.008)

screen = empty('Control monitor',(.67,.6,.5), assembly)
box('Monitor enclosure',(0,0,0),(.97,.13,.66),navy,screen)
box('Display',(0,-.073,0),(.85,.018,.54),screenmat,screen,.025)
box('Monitor foot',(0,.03,-.4),(.32,.3,.08),silver,screen)
box('Monitor stem',(0,.03,-.3),(.08,.08,.3),silver,screen)
for z in [-.15,0,.15]:
    line('Chart guide',[(-.36,-.09,z),(.36,-.09,z)],gridmat,.0025,screen)
for x in [-.3,-.1,.1,.3]:
    line('Chart guide',[(x,-.09,-.18),(x,-.09,.18)],gridmat,.0025,screen)
for i in range(8):
    line('Reference',[(-.35+i*.09,-.093,.10),(-.30+i*.09,-.093,.10)],silver,.003,screen)
response = line('Response',[(0,0,0)]*50,trace,.009,screen)
for i in range(4):
    cylinder('Base indicator',(base[0]-.18+i*.12,base[1]-.31,.16),.017,.012,teal)

bpy.ops.object.camera_add(location=(6,-9,7))
camera=bpy.context.object
target=Vector((0,0,.65))
camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.type='ORTHO'
camera.data.ortho_scale=8.2
scene.camera=camera
right=camera.rotation_euler.to_matrix()@Vector((1,0,0))
up=camera.rotation_euler.to_matrix()@Vector((0,1,0))
assembly.scale=(1.22,)*3
assembly.location=right*1.9 + up*.0
typography=[('Efe Varol',(-3.85,.62),.60,ink),('Bedelcigil',(-3.85,-.05),.60,ink),('Control systems / Robotics',(-3.82,-.59),.19,muted)]
if args.mobile:
    camera.data.ortho_scale=5.2
    assembly.scale=(1.14,)*3
    assembly.location=right*.05-up*1.12
    typography=[('Efe Varol',(-2.35,1.55),.59,ink),('Bedelcigil',(-2.35,.89),.59,ink),('Control systems / Robotics',(-2.33,.40),.17,muted)]
for body,xy,size,mat in typography:
    obj=text('Profile '+body,body,target+right*xy[0]+up*xy[1],size,mat,None)
    obj.rotation_euler=camera.rotation_euler

scan_center=Vector((.25,-.85,.72))+Vector((.25,-.38,.27))
scan_outline=[(-.12,-.07),(.12,-.07),(0,.14),(-.12,-.07)]
scan=line('Inspection scan', [scan_center+right*x+up*y for x,y in scan_outline], scanmat, .005)
scan_sweep=line('Scan sweep', [(0,0,0)]*2, scanmat, .004)

for name,loc,power,size,color in [('Key',(2,-4,7),1100,5,(0.85,.93,1)),('Fill',(-4,-1,4),800,4,(.74,.87,1)),('Rim',(2,5,5),1400,3,(1,.81,.64))]:
    bpy.ops.object.light_add(type='AREA',location=loc)
    light=bpy.context.object
    light.name=name
    light.data.energy=power
    light.data.shape='DISK'
    light.data.size=size
    light.data.color=color
    light.rotation_euler=(Vector((0,0,.5))-light.location).to_track_quat('-Z','Y').to_euler()


def smooth(value):
    value=max(0,min(1,value))
    return value**3*(10-15*value+6*value**2)


poses=[
    (0,(-.10,.06,.5)),(.55,(-.10,.06,.23)),(1.55,(-.10,.06,.23)),
    (1.95,(-.25,-.25,.5)),(2.45,(-.48,-1.07,.23)),(2.95,(-.43,-1.07,.23)),
    (3.30,(-.43,-1.07,.5)),(3.70,(-1.02,-.60,.5)),(4.05,(-1.02,-.60,.21)),
    (4.35,(-1.02,-.60,.21)),(4.65,(-1.02,-.60,.53)),(5.35,(.39,-.56,.53)),
    (5.75,(.39,-.56,.21)),(6.15,(.39,-.56,.21)),(6.50,(.39,-.56,.53)),
    (6.75,(.25,-.85,.72)),(7.02,(.25,-.85,.72)),(7.20,(.39,-.56,.53)),(7.55,(.39,-.56,.21)),
    (7.85,(.39,-.56,.21)),(8.20,(.39,-.56,.53)),(8.90,(-1.02,-.60,.53)),
    (9.20,(-1.02,-.60,.21)),(9.55,(-1.02,-.60,.21)),(9.90,(-1.02,-.60,.5)),
    (10.20,(-.43,-1.07,.5)),(10.45,(-.43,-1.07,.23)),(10.80,(-.48,-1.07,.23)),
    (11.05,(-.48,-1.07,.5)),(11.35,(-.1,.06,.23)),(11.70,(-.1,.06,.23)),
    (12,(-.10,.06,.5))
]


def state(t):
    for (ta,a),(tb,b) in zip(poses,poses[1:]):
        if ta <= t <= tb:
            k=smooth((t-ta)/(tb-ta))
            return Vector(a).lerp(Vector(b),k)
    return Vector(poses[-1][1])


def update(frame):
    t=(frame-1)/15
    end=state(t)
    dx,dy=end.x-base[0],end.y-base[1]
    cos_elbow=max(-.998,min(.998,(dx*dx+dy*dy-l1*l1-l2*l2)/(2*l1*l2)))
    elbow=-math.acos(cos_elbow)
    shoulder=math.atan2(dy,dx)-math.atan2(l2*math.sin(elbow),l1+l2*math.cos(elbow))
    upper.rotation_euler.z=shoulder
    lower.rotation_euler.z=elbow
    wrist.rotation_euler.z=-(shoulder+elbow)
    glance=smooth((t-6.50)/.16)*(1-smooth((t-7.02)/.16))
    inspection.rotation_euler.z=-.7+1.29*glance
    visibility=smooth((t-6.66)/.16)*(1-smooth((t-7.02)/.16))
    fade.inputs[0].default_value=visibility
    scan.hide_render=scan_sweep.hide_render=visibility<.001
    progress=smooth((t-6.66)/.52)
    scan_y=-.07+.21*progress
    half_width=.12*(1-progress)
    for point,x in zip(scan_sweep.data.splines[0].points,[-half_width,half_width]):
        point.co=(*(scan_center+right*x+up*scan_y),1)
    slide.location.z=end.z-.86+.49
    holding=4.15<=t<5.95 or 7.70<=t<9.40
    tuning=.65<t<1.55 or 11.35<t<11.7
    opening=.064 if holding else (.11 if tuning else .13)
    finger_a.location.x=-opening
    finger_b.location.x=opening
    knob.rotation_euler.z=.7*smooth((t-.75)/.7)-.7*smooth((t-11.35)/.35)
    if tuning:
        wrist.rotation_euler.z+=knob.rotation_euler.z
    plaque.location.x=-.48+.05*smooth((t-2.45)/.5)-.05*smooth((t-10.45)/.35)
    plaque.rotation_euler.z=.1*(1-smooth((t-2.45)/.5)) + .1*smooth((t-10.45)/.35)
    if holding:
        chip.location=(end.x,end.y,end.z+.035)
    elif 5.95<=t<7.70:
        chip.location=(.39,-.56,.25)
    else:
        chip.location=(tray[0],tray[1],.25)
    damping=.22+.58*smooth((t-.75)/.7)-.58*smooth((t-11.35)/.35)
    for i,p in enumerate(response.data.splines[0].points):
        u=i/49
        response_y=0 if u<.08 else 1-math.exp(-damping*12*(u-.08))*math.cos(14*(u-.08))
        p.co=(-.36+.72*u,-.105,-.16+.26*response_y,1)


frames=[args.frame] if args.frame else range(args.start,args.end+1)
for frame in frames:
    update(frame)
    scene.render.filepath=str(out/f'{frame:04d}.png')
    bpy.ops.render.render(write_still=True)
    print(f'FRAME {frame}',flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'workbench.blend'))
