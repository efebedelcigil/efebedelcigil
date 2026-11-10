from labels import match_key
import json,html
from pathlib import Path
from build_identity import lettering
from vector_logos import logo
from design_parts import halo,measure,strip_motion
ROOT=Path(__file__).resolve().parents[1]

def build(theme,mobile,groups):
 width=600 if mobile else 1120;columns=2 if mobile else 3;cell=300 if mobile else 374;panel_width=282 if mobile else 354
 dark=theme=='dark';primary='#edf2f8' if dark else '#25394d';muted='#a9b8cc' if dark else '#53677d';fill='#16263b' if dark else '#e4ebf1';line='#2c4059' if dark else '#bdcbd9'
 accents={'teal':'#65c7c2','blue':'#8aa7ff','warm':'#efa571'} if dark else {'teal':'#147c79','blue':'#365d94','warm':'#925c3c'}
 parts=[];top=10
 for row_start in range(0,len(groups),columns):
  heights=[];frames=[]
  for col,g in enumerate(groups[row_start:row_start+columns]):
   x=8+col*cell;y=top;color=accents[match_key(g['color'])];group=[]
   group.append(logo(g['name'],x+2,y,color,size=22));group.append(lettering(g['name'],x+34,y+18,21,primary,600,max_width=panel_width-36))
   bx,by=x+12,y+38
   for j,label in enumerate(g['tools']):
    display=label
    bw=measure(display,19)+51
    if bx+bw>x+panel_width-4:bx=x+12;by+=44
    group.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="34" rx="10" fill="{fill}" stroke="{line}"/>');group.append(halo(bx,by,bw,34,color));group.append(logo(label,bx+10,by+8,muted,fill));group.append(lettering(display,bx+35,by+23,19,primary,550));bx+=bw+8
   h=by-y+50;heights.append(h);frames.append((x,y));parts+=group
  for x,y in frames:parts.append(f'<path d="M{x} {y+30}v{max(heights)-30}h{panel_width}" stroke="{line}" fill="none"/>')
  top+=max(heights)+22
 desc='. '.join(g['name']+': '+', '.join(g['tools']) for g in groups)
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{top}" viewBox="0 0 {width} {top}" role="img"><title>Engineering toolkit</title><desc>{html.escape(desc)}</desc>'+''.join(parts)+'</svg>'
 name='toolkit-'+('mobile-' if mobile else '')+theme
 (ROOT/'assets'/f'{name}.svg').write_text(svg,encoding='utf-8');(ROOT/'assets'/f'{name}-still.svg').write_text(strip_motion(svg),encoding='utf-8')
if __name__=='__main__':
 groups=json.loads((ROOT/'assets/toolkit.json').read_text(encoding='utf-8'))
 for theme in ('dark','light'):
  for mobile in (False,True):build(theme,mobile,groups)
