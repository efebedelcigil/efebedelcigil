from pathlib import Path
import build_identity
build_identity.FONT=Path(__file__).resolve().parents[1]/"assets/fonts/SpaceGrotesk.ttf"
from build_identity import lettering
ROOT=Path(__file__).resolve().parents[1]
for theme in ('dark','light'):
 ink,muted,blue,copper,panel,line=('#edf2f8','#a9b8cc','#78a4ff','#efa571','#142237','#31445e') if theme=='dark' else ('#192a40','#52647a','#214fc5','#b45e30','#edf3fa','#cbd8e8')
 def text(t,x,y,size=24,color=None,weight=550):return lettering(t,x,y,size,color or ink,weight)
 def save(name,w,h,parts):
  (ROOT/'assets'/f'{name}-{theme}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'+''.join(parts)+'</svg>',encoding='utf-8')
 for label in ('GitHub','LinkedIn','Portfolio'):
  save('social-'+label.lower(),180,52,[f'<rect x="1" y="1" width="178" height="50" rx="13" fill="{panel}" stroke="{line}"/>',f'<circle cx="22" cy="26" r="5" fill="{copper if label=="Portfolio" else blue}"/>',text(label,39,34,23),f'<path d="M151 30l8-8m-7 0h7v7" fill="none" stroke="{muted}" stroke-width="2"/>'])
 for mobile in (False,True):
  w=600 if mobile else 1120
  parts=[text('Ege University',8,27,21,muted),text('Electrical & Electronics Engineering',8,65,29),text('Final-year student',8,96,20,muted),f'<path d="M8 122H{w-8}" stroke="{line}"/>']
  parts.extend([text('Control systems',8,169,37,blue,650),text('& robotics',8,211,37,ink,650)])
  x,y=(8,256) if mobile else (580,162)
  for i,row in enumerate(['Embedded systems / Power electronics','Mechatronics / IoT','Circuit design / 3D printing']):parts.append(text(row,x,y+i*31,22,muted))
  parts.append(f'<path d="M{w-130} 20h55l20 20h35M{w-110} 32h28l20 20h48" fill="none" stroke="{line}" stroke-width="2"/>')
  save('focus'+('-mobile' if mobile else ''),w,345 if mobile else 242,parts)
  parts=[text('In progress',8,35,32,blue,650),text('Areas',8,82,20,copper),text('Machine learning / Motor control / Sensing',8,116,22),text('Tools',8,162,20,copper)]
  rows=['Python / VHDL / Verilog','Gazebo / SolidWorks / Fusion'] if mobile else ['Python / VHDL / Verilog / Gazebo / SolidWorks / Fusion']
  for i,row in enumerate(rows):parts.append(text(row,8,196+i*31,22))
  y=274 if mobile else 245
  parts.extend([f'<path d="M8 {y-22}H{w-8}" stroke="{line}"/>',text('Graduation project',8,y+17,22,muted),text('TinyML for control systems',8,y+52,27,ink,650)])
  save('learning'+('-mobile' if mobile else ''),w,y+75,parts)
