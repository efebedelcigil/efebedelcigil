from pathlib import Path
import xml.etree.ElementTree as E
A=Path(__file__).resolve().parents[1]/'assets'
logos={'GitHub':'github','LinkedIn':'linkedin','C':'c','C++':'cplusplus','Python':'python','MATLAB / Simulink':'matlab','Linux':'linux','Git':'git','Gazebo':'gazebo','Verilog':'verilog','Fusion':'fusion','EAGLE':'autodesk','KiCad':'kicad','STM32':'stmicroelectronics','ESP32':'espressif','ROS 2':'ros','Raspberry Pi':'raspberrypi','LTspice':'ltspice','Proteus':'proteus','NanoEdge AI Studio':'stmicroelectronics'}
def logo(label,x,y,c,bg=None):
 path=A/'logos'/(logos.get(label,'_')+'.svg')
 if not path.exists():return f'<path d="M{x+3} {y+2}h12v12H{x+3}zM{x} {y+6}h3m12 0h3M{x+7} {y-1}v3m0 12v3" fill="none" stroke="{c}" stroke-width="1.3"/>'
 r=E.parse(path).getroot();vb=r.get('viewBox','0 0 24 24')
 for e in r.iter():
  for k in ['style','class']:e.attrib.pop(k,None)
  if e.get('fill')!='none':e.set('fill',bg if bg and e.get('fill','').lower() in ('#fff','#ffffff','white') else c)
  if e.get('stroke') and e.get('stroke')!='none':e.set('stroke',c)
  if e.tag.endswith('style'):e.text=''
 r.set('x',str(x));r.set('y',str(y));r.set('width','18');r.set('height','18');r.set('viewBox',vb)
 return E.tostring(r,encoding='unicode')
