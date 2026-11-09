from pathlib import Path
import re
from build_identity import lettering,font_at

def measure(text,size=20,weight=550):
 f=font_at(weight);c=f.getBestCmap();return sum(f['hmtx'][c.get(ord(ch),'.notdef')][0] for ch in text)*size/f['head'].unitsPerEm

def centered(text,width,y,size,color,weight=550):return lettering(text,(width-measure(text,size,weight))/2,y,size,color,weight)

def halo(x,y,w,h,color,still=False):
 if still:return ''
 from math import pi
 perimeter=2*(w+h)-8*10+2*pi*10
 lead=16/perimeter*100;trail=40/perimeter*100
 shape=f'x="{x}" y="{y}" width="{w}" height="{h}" rx="10" pathLength="100" fill="none" stroke="{color}" stroke-width="1"'
 animation='<animate attributeName="stroke-dashoffset" from="0" to="-100" begin="0s" dur="8s" repeatCount="indefinite"/>'
 return f'<rect {shape} opacity=".12"/><rect {shape} stroke-dasharray="{trail:.5f} {100-trail:.5f}" opacity=".15">{animation}</rect><rect {shape} stroke-dasharray="{lead:.5f} {100-lead:.5f}" opacity=".55">{animation}</rect>'

def strip_motion(text):return re.sub(r'<animate\b[^>]*/>','',text)

def branch_groups(groups,width,y,title,ink,muted,accent,panel,line):
 from vector_logos import logo
 parts=[lettering(title,50,y+17,22,accent,600)]
 columns=min(2 if width==600 else 3,len(groups));cell=(width-80)/columns;top=y+48
 for start in range(0,len(groups),columns):
  row=groups[start:start+columns];offset=(columns-len(row))*cell/2;heights=[]
  last_stem=50+offset+(len(row)-1)*cell+4
  parts.append(f'<path d="M22 {y+10}h18M22 {y+10}V{top-16}H{last_stem}" stroke="{line}" fill="none"/>')
  for col,g in enumerate(row):
   gx=50+offset+col*cell
   parts.append(f'<path d="M{gx+4} {top-16}v28h9" stroke="{line}" fill="none"/>');parts.append(logo(g['name'],gx+18,top,accent,size=22));parts.append(lettering(g['name'],gx+46,top+18,21,ink,600))
   bx,by=gx+18,top+34
   for label in g['tools']:
    bw=measure(label,20)+55
    if bx+bw>gx+cell-6:bx=gx+18;by+=48
    parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="36" rx="10" fill="{panel}" stroke="{line}"/>');parts.append(halo(bx,by,bw,36,accent));parts.append(logo(label,bx+10,by+9,muted,panel));parts.append(lettering(label,bx+36,by+25,20,ink,550));bx+=bw+9
   heights.append(by+54-top)
  top+=max(heights)+14
 return parts,top+12
