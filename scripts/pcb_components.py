"""Reusable real-3D renders, projected onto the same board camera."""
from pathlib import Path
from functools import lru_cache
import json,base64

A=Path(__file__).resolve().parents[1]/'assets/components3d'
META=json.loads((A/'layout.json').read_text(encoding='utf-8'))
KINDS=('Empty','Resistor','Capacitor','Inductor','IC')

def scale(chip):return chip.width/12,chip.height/18

def contacts(chip,x,y,level):
 sx,sy=scale(chip);points=META['parts'][str(level)]['contacts'] if level else [(-5.2,0),(5.2,0)]
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

ORIENTATIONS={}
PAD_TURNS={}
SCALES={}
from dataclasses import replace
def scaled_chip(chip,x,y,level):
 k=SCALES.get((round(x,6),round(y,6),level),1)
 return replace(chip,width=chip.width*k,height=chip.height*k)
def variant_at(x,y,level):return ORIENTATIONS.get((round(x,6),round(y,6),level),level)
_original_contacts=contacts
_original_component=component
def oriented_contacts(chip,x,y,level):return _original_contacts(scaled_chip(chip,x,y,level),x,y,variant_at(x,y,level))
def oriented_component(chip,x,y,level,*args):return _original_component(scaled_chip(chip,x,y,level),x,y,variant_at(x,y,level),*args)
contacts=oriented_contacts;component=oriented_component
def empty_lands(chip,x,y,level,panel,metal,copper):
 if level:return ''
 angle=PAD_TURNS.get((round(x,6),round(y,6)),0)
 result=f'<g data-empty-lands="true" transform="translate({x} {y}) rotate({angle})">'
 for px in [-5.2,5.2]:
  result+=f'<rect x="{px-1.55}" y="-2.6" width="3.1" height="5.2" rx=".5" fill="#897553" opacity=".60"/><rect x="{px-1.15}" y="-2.2" width="2.3" height="4.4" rx=".3" fill="#c0c8bc" opacity=".85"/>'
 return result+'</g>'
pads=empty_lands



def body_origin(chip,level):
 if not level:return 0,0
 px,py=META['parts'][str(level)]['body_screen_center'];ia,ib,ic,id=META['inverse']
 return -(ia*px+ic*py)*chip.width/12,-(ib*px+id*py)*chip.height/18
