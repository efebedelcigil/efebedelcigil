"""Recognizable through-hole components and their physical contact pads."""
from math import sin,cos,pi
from hashlib import sha256

KINDS=('Empty','Resistor','Capacitor','Inductor','IC')

def contacts(chip,x,y,level):
 cx=x+chip.width/2;cy=y+chip.height/2
 if level==4:return [(x-3,y+v) for v in [2.5,5.5,8.5,11.5]]+[(x+chip.width+3,y+v) for v in [2.5,5.5,8.5,11.5]]
 if level==2:return [(cx-3,cy+6),(cx+3,cy+6)]
 return [(x-3,cy),(x+chip.width+3,cy)]

def pads(chip,x,y,level,panel,metal,copper):
 opacity=.75 if level else .22
 result=f'<g data-contact-pads="{level}" opacity="{opacity}">'
 for px,py in contacts(chip,x,y,level):
  result+=f'<ellipse cx="{px}" cy="{py}" rx="1.4" ry="1.1" fill="{metal}"/><ellipse cx="{px}" cy="{py}" rx=".55" ry=".42" fill="{panel}"/>'
 return result+'</g>'

def component(chip,x,y,level,panel,metal,copper,ink):
 if not level:return ''
 cx=x+chip.width/2;cy=y+chip.height/2;lift=chip.lift(level)
 gid='material'+sha256(f'{x},{y},{level}'.encode()).hexdigest()[:12]
 result=[f'<defs><linearGradient id="{gid}r" x2="0" y2="1"><stop stop-color="#8f714e"/><stop offset=".35" stop-color="#ebd4a7"/><stop offset=".7" stop-color="#c0a174"/><stop offset="1" stop-color="#876943"/></linearGradient><linearGradient id="{gid}c"><stop stop-color="#17394f"/><stop offset=".35" stop-color="#6797ad"/><stop offset=".65" stop-color="#38667f"/><stop offset="1" stop-color="#18394d"/></linearGradient><linearGradient id="{gid}m"><stop stop-color="#72888d"/><stop offset=".4" stop-color="#d5ddcf"/><stop offset="1" stop-color="#879b9c"/></linearGradient><linearGradient id="{gid}i" x2="1" y2="1"><stop stop-color="#50626b"/><stop offset=".35" stop-color="#34454f"/><stop offset="1" stop-color="#1b2931"/></linearGradient></defs>']
 shadow_rx=5.6 if level==3 else chip.width*.55
 result.append(f'<ellipse data-contact-shadow="true" cx="{cx+1.2}" cy="{cy+(.9 if level==1 else 2.7)}" rx="{shadow_rx}" ry="{.9 if level==1 else (2.3 if level!=4 else chip.height*.45)}" fill="#061a12" opacity=".3"/>')
 if level==4:
  for py in [2.5,5.5,8.5,11.5]:result.append(f'<path d="M{x-3} {y+py}h1v{-lift}h2M{x+chip.width+3} {y+py}h-1v{-lift}h-2" fill="none" stroke="{metal}" stroke-width="1.2" stroke-linejoin="round"/>')
 elif level==2:result.append(f'<path d="M{cx-3} {cy+6}v-5m6 5v-5" stroke="{metal}" stroke-width="1"/>')
 else:result.append(f'<path d="M{x-3} {cy}h{chip.width+6}" stroke="{metal}" stroke-width="1.1"/>')
 # A concave meniscus and one highlight suggest solder without large shiny blobs.
 for px,py in contacts(chip,x,y,level):
  result.append(f'<path data-solder="true" d="M{px-1.2} {py+.6}Q{px-.4} {py+.1} {px-.4} {py-.6}h.8Q{px+.4} {py+.1} {px+1.2} {py+.6}Z" fill="{metal}"/><path d="M{px-.7} {py+.3}Q{px} {py-.2} {px+.7} {py+.3}" fill="none" stroke="{ink}" stroke-width=".3" opacity=".6"/>')
 if level==1:
  result.append(f'<path d="M{x} {cy-1.7}Q{x+1} {cy-2.8} {x+2} {cy-2}H{x+chip.width-2}Q{x+chip.width+1} {cy-2.8} {x+chip.width} {cy+1.7}Q{x+chip.width-1} {cy+2.8} {x+chip.width-2} {cy+2}H{x+2}Q{x-1} {cy+2.8} {x} {cy-1.7}Z" fill="url(#{gid}r)" stroke="#937957" stroke-width=".4"/>')
  for offset,color in [(1.8,'#684334'),(3.5,'#26323b'),(5.4,'#a17630')]:result.append(f'<path d="M{x+offset} {cy-2}v4" stroke="{color}" stroke-width="1"/>')
 elif level==2:
  result.append(f'<g transform="matrix(1 0 .24 1 {-0.24*(cy+2)} 0)"><ellipse cx="{cx}" cy="{cy+2}" rx="4.2" ry="2" fill="#233d50"/><path d="M{cx-4.2} {cy-7}v9a4.2 2 0 0 0 8.4 0v-9z" fill="url(#{gid}c)"/><path d="M{cx+2.3} {cy-7}v10" stroke="{metal}" stroke-width="1.3"/><ellipse cx="{cx}" cy="{cy-7}" rx="4.2" ry="2.2" fill="url(#{gid}m)"/><path d="M{cx-2} {cy-8}l4 2m-4 0l4 -2" stroke="#445969" stroke-width=".5"/></g>')
 elif level==3:
  result.append(f'<circle cx="{cx}" cy="{cy+1.5}" r="3.5" fill="none" stroke="#1e302c" stroke-width="3.5"/><circle cx="{cx}" cy="{cy}" r="3.5" fill="none" stroke="#34464e" stroke-width="3.5"/>')
  for i in range(9):
   a=i*2*pi/9;ax=cx+2.1*cos(a);ay=cy+2.1*sin(a);bx=cx+5.2*cos(a+.12);by=cy+5.2*sin(a+.12)
   result.append(f'<path d="M{ax} {ay}Q{cx+5.6*cos(a-.12)} {cy+5.6*sin(a-.12)} {bx} {by}" fill="none" stroke="#a36934" stroke-width="2.1" stroke-linecap="round"/><path d="M{ax} {ay}Q{cx+5.6*cos(a-.12)} {cy+5.6*sin(a-.12)} {bx} {by}" fill="none" stroke="{copper}" stroke-width="1.1" stroke-linecap="round"/>')
 else:
  result.append(f'<path d="M{x} {y+chip.height-lift}h{chip.width}v{lift}h{-chip.width}z" fill="#273b45"/><path d="M{x+chip.width} {y-lift}l1.2 1v{chip.height+lift-1}l-1.2 {-lift}z" fill="#1e2a32"/><rect x="{x}" y="{y-lift}" width="{chip.width}" height="{chip.height}" rx=".5" fill="url(#{gid}i)" stroke="{metal}" stroke-width=".4"/><path d="M{cx-1.4} {y-lift}q1.4 2.5 2.8 0" fill="none" stroke="{metal}" stroke-width=".65"/><circle cx="{x+1.3}" cy="{y-lift+2}" r=".5" fill="{metal}"/><path d="M{x+2} {y-lift+6}h4m-4 2h3m-3 2h4" stroke="{metal}" stroke-width=".55" opacity=".75"/>')
 return ''.join(result)
