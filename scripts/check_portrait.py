import json
import math
from pathlib import Path
import runpy
import sys
import bpy
from mathutils.bvhtree import BVHTree

root=Path(__file__).resolve().parents[1]
sys.argv=['blender','--','--out',str(root/'.render/portrait-check'),'--frame','55']
model=runpy.run_path(str(root/'scripts/render_portrait.py'))
objects=model['model']
update=model['update']


def snapshot(t):
    update(t*24+1)
    row=[]
    for name in ('yaw','upper','lower','wrist_pitch','wrist','inspection','finger_a','finger_b','knob','chip'):
        obj=objects[name]
        row.extend(obj.location)
        row.extend(obj.rotation_euler)
    row.extend(model['camera'].location)
    row.extend(model['camera'].rotation_euler)
    row.append(model['camera'].data.lens)
    row.append(objects['fade'].inputs[0].default_value)
    for point in objects['response'].data.splines[0].points:
        row.extend(point.co)
    return row


first=snapshot(2.25)
last=snapshot(23.25)
loop_error=max(abs(a-b) for a,b in zip(first,last))
assert loop_error<1e-5,loop_error
assert max(abs(a-b) for a,b in zip(first,snapshot(18.25)))<1e-5
previous=snapshot(0)
fixed_camera=tuple(model['camera'].location)+tuple(model['camera'].rotation_euler)+(model['camera'].data.lens,)
maximum_step=0
maximum_fk_error=0
for index in range(1,2791):
    t=index/120
    current=snapshot(t)
    assert tuple(model['camera'].location)+tuple(model['camera'].rotation_euler)+(model['camera'].data.lens,)==fixed_camera
    assert all(math.isfinite(value) for value in current)
    maximum_step=max(maximum_step,max(abs(a-b) for a,b in zip(current,previous)))
    previous=current
    target=model['core']['state'](t)
    angle=objects['yaw'].rotation_euler.z
    shoulder=-objects['upper'].rotation_euler.y
    elbow=-objects['lower'].rotation_euler.y
    radius=objects['l1']*math.cos(shoulder)+objects['l2']*math.cos(shoulder+elbow)
    x=objects['base'][0]+radius*math.cos(angle)-model['offset']*math.sin(angle)
    y=objects['base'][1]+radius*math.sin(angle)+model['offset']*math.cos(angle)
    z=.56+objects['l1']*math.sin(shoulder)+objects['l2']*math.sin(shoulder+elbow)-.49
    maximum_fk_error=max(maximum_fk_error,math.sqrt((x-target.x)**2+(y-target.y)**2+(z-target.z)**2))
assert maximum_step<.15,maximum_step
assert maximum_fk_error<1e-5,maximum_fk_error

def child(parent,name):
    return next(obj for obj in parent.children if obj.name.startswith(name))

upper=child(objects['upper'],'Contoured robot link')
lower=child(objects['lower'],'Contoured robot link')
gripper=child(objects['slide'],'Electric gripper')
camera=child(objects['inspection'],'Stereo inspection enclosure')
flange=child(objects['wrist'],'Tool flange')
base=bpy.data.objects['Servo drive']
pairs=[(upper,lower),(upper,gripper),(upper,camera),(upper,flange),(lower,base),(gripper,base),(camera,base),(camera,flange),(camera,gripper)]
monitor=child(objects['screen'],'Monitor enclosure')
shoe=bpy.data.objects['Machined mounting shoe']
pairs.extend((monitor,obj) for obj in (upper,lower,gripper,camera,flange,base,shoe))
pcb=bpy.data.objects['PCB']
pairs.extend((pcb,obj) for obj in (upper,lower,gripper,camera,flange,base,monitor))
chip=objects['chip']
pairs.extend((chip,obj) for obj in (upper,lower,camera,pcb,base,monitor,gripper))
collisions=[]
for frame in range(1,560):
    update(frame)
    bpy.context.view_layer.update()
    trees={}
    for obj in {obj for pair in pairs for obj in pair}:
        assert not obj.hide_render,obj.name
        vertices=[obj.matrix_world@v.co for v in obj.data.vertices]
        trees[obj]=BVHTree.FromPolygons(vertices,[tuple(face.vertices) for face in obj.data.polygons])
    for a,b in pairs:
        if trees[a].overlap(trees[b]):
            collisions.append({'frame':frame,'a':a.name,'b':b.name})
assert not collisions,collisions[:12]
assert not bpy.data.objects['PCB'].hide_render
assert all(obj.hide_render for obj in bpy.data.objects if obj.name.startswith(('Public activity LED','Inspection scan','Scan sweep')))
for boundary in (3.95,6.35,8.10,10.35):
    update((boundary-1e-6)*24+1)
    before=objects['chip'].location.copy()
    update((boundary+1e-6)*24+1)
    assert (before-objects['chip'].location).length<1e-5,boundary
update(14.25*24+1)
low_peak=max(p.co.z for p in objects['response'].data.splines[0].points)
update(16.4*24+1)
high_peak=max(p.co.z for p in objects['response'].data.splines[0].points)
assert low_peak-high_peak>.10,(low_peak,high_peak)
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
anchor=Vector((*objects['base'],.56))
model['projection']('background',2.25)
bpy.context.view_layer.update()
reference_anchor=world_to_camera_view(bpy.context.scene,model['camera'],anchor)
background_state=tuple(model['camera'].matrix_world[i][j] for i in range(4) for j in range(4))
anchor_error=0
for t in (18.25,18.75,18.80,19.0,19.45,19.8,20.35,21.25,21.75,22.25,23.25):
    model['projection']('background',t)
    bpy.context.view_layer.update()
    assert tuple(model['camera'].matrix_world[i][j] for i in range(4) for j in range(4))==background_state
    assert model['camera'].data.type=='ORTHO' and abs(model['camera'].data.ortho_scale-4.10)<1e-5
    model['projection']('glance',t)
    bpy.context.view_layer.update()
    projected=world_to_camera_view(bpy.context.scene,model['camera'],anchor)
    anchor_error=max(anchor_error,abs(projected.x-reference_anchor.x),abs(projected.y-reference_anchor.y))
assert anchor_error<1e-4,anchor_error
report={'samples':2791,'sample_rate_hz':120,'startup_seconds':2.25,'loop_seconds':132,'work_seconds':16,'glance_seconds':5,
        'loop_state_error':loop_error,'maximum_step':maximum_step,
        'maximum_fk_error':maximum_fk_error,'collision_frames_checked':559,'nonadjacent_pairs':len(pairs),
        'surface_intersections':collisions,'response_peak_difference':low_peak-high_peak,'chip_transfer_continuity':True,'fixed_station_projection':True,'shoulder_anchor_projection_error':anchor_error,'pcb_visible':True,'scan_removed':True,
        'scope':'Visible joint, camera, gripper, dial and control-display continuity; not a physics simulation.'}
(root/'.render/portrait-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report),flush=True)
