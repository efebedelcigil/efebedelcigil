import json
import math
from pathlib import Path
import runpy
import sys

import bpy
from mathutils import Vector


root=Path(__file__).resolve().parents[1]
arguments=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--out',required=True,type=Path)
parser.add_argument('--frame',type=int)
parser.add_argument('--start',type=int,default=1)
parser.add_argument('--end',type=int,default=559)
parser.add_argument('--layered',action='store_true')
parser.add_argument('--width',type=int,default=900)
args=parser.parse_args(arguments)
sys.argv=['blender','--','--out',str(args.out),'--end','0','--width',str(args.width)]
model=runpy.run_path(str(root/'scripts/render_workbench.py'))
core=model['update'].__globals__
keep={model['yaw'],*model['yaw'].children_recursive,model['knob'],*model['knob'].children_recursive,
      model['screen'],*model['screen'].children_recursive,model['scan'],model['scan_sweep']}
base_names=('Machined mounting shoe','Turntable','Servo drive','Drive seal','Anchor bolt','Base indicator')
for obj in bpy.context.scene.objects:
    if obj.type in ('MESH','CURVE','FONT') and obj not in keep and not obj.name.startswith(base_names):
        obj.hide_render=True
offset=.50
model['lower'].location.y=offset
model['inspection'].location.y=-.20
neck=core['cylinder']('Camera swivel mount',(0,-.17,-.06),.045,.23,model['polished'],model['wrist'])
neck.rotation_euler.x=math.pi/2
lens_coating=core['material']('Optical coating',(.012,.06,.18),.72,.10)
for obj in model['inspection'].children:
    if obj.name.startswith('Optical glass'):
        obj.data.materials.clear()
        obj.data.materials.append(lens_coating)
for x in (-.065,.065):
    iris=core['cylinder']('Lens inner element',(x,-.229,0),.017,.006,model['navy'],model['inspection'])
    iris.rotation_euler.x=math.pi/2
axle=core['cylinder']('Elbow cross shaft',(model['l1'],offset/2,0),.105,offset,model['polished'],model['upper'])
axle.rotation_euler.x=math.pi/2
for obj in model['upper'].children:
    if obj.name.startswith(('Power harness','Sensor loom')):
        for point in obj.data.splines[0].points:
            point.co.y=-point.co.y
model['knob'].location=(-.30,-.10,.16)
bracket=core['box']('Button mounting arm',(-.50,.035,.105),(.70,.23,.09),model['navy'])
bracket.rotation_euler.z=-.55
model['screen'].location=(.95,.45,.70)
model['screen'].scale=(.80,)*3
core['box']('Monitor pedestal foot',(.95,.47,.04),(.42,.38,.08),model['navy'])
core['box']('Monitor pedestal column',(.95,.47,.20),(.075,.075,.32),model['silver'])
pcb_names=('PCB','Integrated circuit','IC pin','SMD resistor','Resistor terminal','Capacitor','USB port','USB socket','Header insulator','Header pin','Test socket pad','Signal trace','Plated via','Board mount')
for obj in bpy.context.scene.objects:
    if obj.name.startswith(pcb_names):
        obj.hide_render=False
core['box']('PCB fixture',(.43,-.61,.065),(1.18,.80,.08),model['silver'])
for x in (-.04,.90):
    for y in (-.90,-.32):
        core['cylinder']('Fixture foot',(x,y,.035),.055,.07,model['navy'])
scene=bpy.context.scene
scene.render.resolution_y=round(args.width*1.2)
camera=model['camera']
target=Vector((.0,.0,.95))
camera.location=target+Vector((7,-9,6.5))
camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.type='ORTHO'
camera.data.ortho_scale=4.10
camera.data.shift_x=camera.data.shift_y=0
camera.data.clip_start=.03
right=camera.rotation_euler.to_matrix()@Vector((1,0,0))
up=camera.rotation_euler.to_matrix()@Vector((0,1,0))
core['right'],core['up']=right,up
park=(.15,-.35,.85)
source=(.39,-.56,.22)
tray=(-.27,-.68,.22)
model['chip'].hide_render=False
core['box']('Transfer socket',(.39,-.56,.19),(.19,.19,.04),model['navy'])
core['box']('Transfer tray',(-.27,-.68,.17),(.28,.28,.08),model['silver'])
core['box']('Component lid',(0,0,.047),(.10,.10,.012),model['blue'],model['chip'],.008)
for side in (-1,1):
    for pin in range(3):
        core['box']('Component terminal',(side*.073,-.04+pin*.04,-.025),(.02,.015,.025),model['polished'],model['chip'],.002)
for obj in model['screen'].children:
    if obj.name.startswith('Reference'):
        for point in obj.data.splines[0].points:
            point.co.z=.03
core['poses']=[
    (0,(.25,.05,.65)),(.6,(-.30,-.10,.23)),(1.6,(-.30,-.10,.23)),(2.25,park),
    (3.1,(source[0],source[1],.60)),(3.7,source),(4.05,source),
    (4.85,(source[0],source[1],.60)),(5.65,(tray[0],tray[1],.60)),
    (6.25,tray),(6.55,tray),(7.0,(tray[0],tray[1],.48)),(7.4,(tray[0],tray[1],.55)),
    (7.85,tray),(8.15,tray),(8.85,(tray[0],tray[1],.60)),
    (9.65,(source[0],source[1],.60)),(10.25,source),(10.55,source),
    (11.2,(source[0],source[1],.60)),(12.2,(-.30,-.10,.23)),
    (17.05,(-.30,-.10,.23)),(18.25,park),
    (18.65,(.20,-.40,.85)),(19.35,(.50,-.60,1.08)),(21.5,(.50,-.60,1.08)),
    (22.4,(.20,-.45,.85)),(23.25,park)
]
smooth=core['smooth']
core_update=core['update']


def update(frame):
    core_update(frame)
    model['scan'].hide_render=model['scan_sweep'].hide_render=True
    model['fade'].inputs[0].default_value=0
    t=(frame-1)/24
    end=core['state'](t)
    dx,dy=end.x-model['base'][0],end.y-model['base'][1]
    radial_squared=dx*dx+dy*dy-offset*offset
    if radial_squared<=0:
        raise ValueError('Target lies inside the offset wrist exclusion radius.')
    radial=math.sqrt(radial_squared)
    height=end.z+.49-.56
    cosine=(radial*radial+height*height-model['l1']**2-model['l2']**2)/(2*model['l1']*model['l2'])
    if not -.998<cosine<.998:
        raise ValueError('Target exceeds the articulated arm workspace.')
    elbow=-math.acos(cosine)
    shoulder=math.atan2(height,radial)-math.atan2(model['l2']*math.sin(elbow),model['l1']+model['l2']*math.cos(elbow))
    model['yaw'].rotation_euler.z=math.atan2(dy,dx)-math.atan2(offset,radial)
    model['upper'].rotation_euler.y=-shoulder
    model['lower'].rotation_euler.y=-elbow
    model['wrist_pitch'].rotation_euler.y=shoulder+elbow
    contact=sum(smooth((t-a)/.2)*(1-smooth((t-b)/.3)) for a,b in [(.45,1.6),(12.2,17.05)])
    grasp=smooth((t-3.72)/.23)*(1-smooth((t-6.35)/.17))+smooth((t-7.90)/.20)*(1-smooth((t-10.35)/.17))
    opening=.17-.0175*contact-.0775*grasp
    model['finger_a'].location.x=-opening
    model['finger_b'].location.x=opening
    angle=.75*smooth((t-.75)/.65)-1.60*smooth((t-13.0)/1.25)+1.60*smooth((t-15.25)/1.15)
    model['knob'].rotation_euler.z=angle
    button=smooth((t-.5)/.16)*(1-smooth((t-1.6)/.2))
    bpy.data.objects['Dial'].location.z=.03-.022*button
    bpy.data.objects['Dial marker'].location.z=-.022*button
    turn=sum(smooth((t-a)/.25)*(1-smooth((t-b)/.35)) for a,b in [(.4,1.6),(11.9,17.05)])
    model['wrist'].rotation_euler.z=-model['yaw'].rotation_euler.z+angle*turn
    look=smooth((t-18.8)/.3)*(1-smooth((t-21.9)/.5))
    tilt=smooth((t-19.65)/.13)*(1-smooth((t-20.35)/.25))
    model['inspection'].rotation_euler.z=-.25+1.10*look
    model['inspection'].rotation_euler.y=math.radians(17)*tilt
    model['inspection'].rotation_euler.x=-.49*look
    if 3.95<=t<6.35 or 8.10<=t<10.35:
        model['chip'].location=end+Vector((0,0,.035))
    else:
        location=tray if 6.35<=t<8.10 else source
        model['chip'].location=(location[0],location[1],location[2]+.035)
    damping=.12+.88*max(0,min(1,(angle+.85)/1.60))
    for i,p in enumerate(model['response'].data.splines[0].points):
        u=i/49
        elapsed=max(0,(u-.06)*12)
        omega=1.6
        if damping>=.999:
            response=1-(1+omega*elapsed)*math.exp(-omega*elapsed)
        else:
            root_damping=math.sqrt(1-damping*damping)
            phase=omega*root_damping*elapsed
            response=1-math.exp(-damping*omega*elapsed)*(math.cos(phase)+damping/root_damping*math.sin(phase))
        p.co=(-.36+.72*u,-.105,-.19+.22*response,1)


original_visibility={obj:obj.hide_render for obj in bpy.context.scene.objects if obj.type in ('MESH','CURVE','FONT')}
moving={model['yaw'],*model['yaw'].children_recursive,model['chip'],*model['chip'].children_recursive,
        bpy.data.objects['Dial'],bpy.data.objects['Dial marker'],model['response']}

arm={model['yaw'],*model['yaw'].children_recursive}

def visibility(mode):
    for obj,hidden in original_visibility.items():
        selected=moving if mode in ('background','foreground') else arm
        obj.hide_render=hidden or (mode in ('background','glance-background') and obj in selected) or (mode in ('foreground','glance') and obj not in selected)
    model['scan'].hide_render=model['scan_sweep'].hide_render=True

def projection(mode,t):
    camera.data.shift_x=camera.data.shift_y=0
    camera.data.type='ORTHO'
    camera.data.ortho_scale=4.10
    camera.location=target+Vector((7,-9,6.5))
    camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
    emphasis=smooth((t-18.75)/.70)*(1-smooth((t-21.25)/1.0)) if mode=='glance' else 0
    if emphasis>1e-6:
        direction=Vector((7,-9,6.5)).normalized()
        distance=1/((1-emphasis)/400+emphasis/1.85)
        shoulder=Vector((*model['base'],.56))
        anchor_depth=distance+direction.dot(target-shoulder)
        camera.data.type='PERSP'
        camera.data.sensor_fit='VERTICAL'
        camera.data.sensor_height=32
        camera.data.lens=anchor_depth*32/4.10
        camera.location=target+direction*distance
        camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()

if args.layered:
    update(55)
    for mode,name in [('full','portrait-steady.png'),('background','portrait-background.png'),('glance-background','portrait-glance-background.png')]:
        visibility(mode)
        projection(mode,2.25)
        scene.render.filepath=str(args.out.parent/name)
        bpy.ops.render.render(write_still=True)
frames=[args.frame] if args.frame else range(args.start,args.end+1)
for frame in frames:
    update(frame)
    mode=('foreground' if frame<=438 else 'glance') if args.layered else 'full'
    visibility(mode)
    projection(mode,(frame-1)/24)
    scene.render.filepath=str(args.out/f'{frame:04d}.png')
    bpy.ops.render.render(write_still=True)
    print(f'PORTRAIT {frame}',flush=True)
