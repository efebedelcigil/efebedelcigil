"""Reusable real-3D renders, projected onto the same board camera."""
from pathlib import Path
from functools import lru_cache
import json,base64

A=Path(__file__).resolve().parents[1]/'assets/components3d'
META=json.loads((A/'layout.json').read_text(encoding='utf-8'))
KINDS=('Empty','Resistor','Capacitor','Inductor','IC')

def scale(chip):return chip.width/12,chip.height/18

def contacts(chip,x,y,level):
 sx,sy=scale(chip);points=META['parts'][str(level)]['contacts'] if level else [(-9,0),(9,0)]
 return [(x+px*sx,y+py*sy) for px,py in points]

@lru_cache(maxsize=1)
def definitions():
 parts=['<defs>']
 for level,p in META['parts'].items():
  encoded=base64.b64encode((A/f'part-{level}.png').read_bytes()).decode()
  width=round(p['image'][2]/META['units_per_pixel']);height=round(p['image'][3]/META['units_per_pixel'])
  parts.append(f'<symbol id="physicalPart{level}" viewBox="0 0 {width} {height}"><image width="{width}" height="{height}" href="data:image/png;base64,{encoded}"/></symbol>')
 return ''.join(parts)+'</defs>'

def pads(chip,x,y,level,panel,metal,copper):
 if level:return ''
 result='<g data-contact-pads="0" opacity=".55">'
 for px,py in contacts(chip,x,y,level):result+=f'<ellipse cx="{px}" cy="{py}" rx="1.65" ry="1.25" fill="{metal}"/><ellipse cx="{px}" cy="{py}" rx=".65" ry=".5" fill="{panel}"/>'
 return result+'</g>'

def component(chip,x,y,level,panel,metal,copper,ink):
 if not level:return ''
 sx,sy=scale(chip);p=META['parts'][str(level)];ix,iy,w,h=p['image'];ia,ib,ic,id=META['inverse']
 return f'<g data-component-sprite="{level}" transform="translate({x} {y}) scale({sx} {sy})"><g transform="matrix({ia} {ib} {ic} {id} 0 0)"><use href="#physicalPart{level}" x="{ix}" y="{iy}" width="{w}" height="{h}"/></g></g>'
