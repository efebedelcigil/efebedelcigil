import json,html
from pathlib import Path
from build_identity import lettering
from vector_logos import logo
from design_parts import halo,measure,strip_motion
ROOT=Path(__file__).resolve().parents[1]

def build(theme,mobile,groups):
 width=600 if mobile else 1120;columns=2 if mobile else 3;cell=300 if mobile else 374;panel_width=282 if mobile else 354
 dark=theme=='dark';primary='#edf2f8' if dark else '#192a40';muted='#a9b8cc' if dark else '#52647a';fill='#16263b' if dark else '#edf3fa';line='#2c4059' if dark else '#d0ddeb'
 accents={'teal':'#65c7c2','blue':'#8aa7ff','warm':'#efa571'} if dark else {'teal':'#147c79','blue':'#365dc1','warm':'#a75a2c'}
 icons={'code':'M2 4L-3 9l5 5m8-10 5 5-5 5M8 2 5 16','wave':'M-3 10c5-16 8 16 13 0s8 0 8 0','chip':'M0 3h14v14H0zM4 0v3m6-3v3M4 17v3m6-3v3M-3 7h3m-3 6h3m14-6h3m-3 6h3','circuit':'M-3 5h8l6 10h8M-3 15h8l6-10h8','logic':'M0 3v14h5c12 0 12-14 0-14zM-4 6h4m-4 8h4m13-4h7','terminal':'M-2 3l6 6-6 6m9 0h9'}
 parts=[];top=10
 for row_start in range(0,len(groups),columns):
  heights=[]
  for col,g in enumerate(groups[row_start:row_start+columns]):
   x=8+col*cell;y=top;color=accents[g['color']];group=[]
   group.append(f'<g transform="translate({x+5} {y+1})" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"><path d="{icons[g["icon"]]}"/></g>');group.append(lettering(g['name'],x+34,y+18,21,primary,600))
   bx,by=x+12,y+38
   for j,label in enumerate(g['tools']):
    bw=measure(label,19)+51
    if bx+bw>x+panel_width-4:bx=x+12;by+=44
    group.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="34" rx="10" fill="{fill}" stroke="{line}"/>');group.append(halo(bx,by,bw,34,color,j*13));group.append(logo(label,bx+10,by+8,muted,fill));group.append(lettering(label,bx+35,by+23,19,primary,550));bx+=bw+8
   h=by-y+50;heights.append(h);parts.append(f'<path d="M{x} {y+30}v{h-30}h{panel_width}" stroke="{line}" fill="none"/>');parts+=group
  top+=max(heights)+22
 desc='. '.join(g['name']+': '+', '.join(g['tools']) for g in groups)
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{top}" viewBox="0 0 {width} {top}" role="img"><title>Engineering toolkit</title><desc>{html.escape(desc)}</desc>'+''.join(parts)+'</svg>'
 name='toolkit-'+('mobile-' if mobile else '')+theme
 (ROOT/'assets'/f'{name}.svg').write_text(svg,encoding='utf-8');(ROOT/'assets'/f'{name}-still.svg').write_text(strip_motion(svg),encoding='utf-8')
if __name__=='__main__':
 groups=json.loads((ROOT/'assets/toolkit.json').read_text(encoding='utf-8'))
 for theme in ('dark','light'):
  for mobile in (False,True):build(theme,mobile,groups)
