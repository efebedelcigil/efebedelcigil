import json
import math
import runpy
import sys
from pathlib import Path

import bpy


root = Path(__file__).resolve().parents[1]
sys.argv = ['blender', '--', '--out', str(root/'.render/check'), '--frame', '1']
model = runpy.run_path(str(root/'scripts/render_workbench.py'))
update, state = model['update'], model['state']
samples = []
maximum_error = 0
minimum_margin = 10
for index in range(1441):
    t = index/120
    update(t*15+1)
    end = state(t)
    shoulder = model['upper'].rotation_euler.z
    elbow = model['lower'].rotation_euler.z
    l1, l2 = model['l1'], model['l2']
    x = model['base'][0]+l1*math.cos(shoulder)+l2*math.cos(shoulder+elbow)
    y = model['base'][1]+l1*math.sin(shoulder)+l2*math.sin(shoulder+elbow)
    error = math.hypot(x-end.x,y-end.y)
    maximum_error = max(maximum_error,error)
    reach = math.hypot(end.x-model['base'][0],end.y-model['base'][1])
    minimum_margin = min(minimum_margin,l1+l2-reach,reach-abs(l1-l2))
    row = [*end,shoulder,elbow,model['inspection'].rotation_euler.z,
           model['knob'].rotation_euler.z,*model['chip'].location,
           model['plaque'].location.x,model['plaque'].rotation_euler.z,
           model['fade'].inputs[0].default_value]
    assert all(math.isfinite(value) for value in row)
    samples.append(row)
assert maximum_error < 1e-5, maximum_error
assert minimum_margin > .01, minimum_margin
loop_error = max(abs(a-b) for a,b in zip(samples[0],samples[-1]))
assert loop_error < 1e-5, loop_error
maximum_joint_step=max(abs(b[axis]-a[axis]) for a,b in zip(samples,samples[1:]) for axis in (3,4))
assert maximum_joint_step < .15, maximum_joint_step
for t in (4.15,5.95,7.70,9.40):
    update((t-1e-6)*15+1)
    before=model['chip'].location.copy()
    update((t+1e-6)*15+1)
    assert (before-model['chip'].location).length < .006
for t,_ in model['poses'][1:-1]:
    h=1e-5
    velocity=(state(t+h)-state(t-h))/(2*h)
    assert velocity.length < .02, (t,velocity.length)
    h=.001
    acceleration=(state(t+h)-2*state(t)+state(t-h))/(h*h)
    assert acceleration.length < .8, (t,acceleration.length)
report={
    'duration_seconds':12,
    'sample_rate_hz':120,
    'samples':len(samples),
    'maximum_ik_error':maximum_error,
    'minimum_workspace_margin':minimum_margin,
    'loop_state_error':loop_error,
    'maximum_joint_step_rad_at_120_hz':maximum_joint_step,
    'checked':['finite transforms','unclamped reachable targets','zero endpoint velocity and acceleration',
               'joint and camera loop closure','component handoffs','overlay fade closure'],
    'scope':'Kinematic continuity; not a physics or hardware safety certification.'
}
target=root/'.render/motion-check.json'
target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report),flush=True)
