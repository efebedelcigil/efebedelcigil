from labels import display_label
from pathlib import Path
import re
from build_identity import lettering,font_at

def measure(text,size=20,weight=550):
 text=display_label(text)
 f=font_at(weight);c=f.getBestCmap();return sum(f['hmtx'][c.get(ord(ch),'.notdef')][0] for ch in text)*size/f['head'].unitsPerEm

def centered(text,width,y,size,color,weight=550):return lettering(text,(width-measure(text,size,weight))/2,y,size,color,weight)

def halo(x,y,w,h,color,still=False,radius=10):
 if still:return ''
 from math import pi
 perimeter=2*(w+h)-8*10+2*pi*10
 lead=12;trail=28
 shape=f'x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" pathLength="100" fill="none" stroke="{color}" stroke-width="1"'
 animation='<animate attributeName="stroke-dashoffset" from="0" to="-100" begin="0s" dur="8s" repeatCount="indefinite"/>'
 return f'<rect {shape} opacity=".12"/><rect {shape} stroke-dasharray="{trail:.5f} {100-trail:.5f}" opacity=".15">{animation}</rect><rect {shape} stroke-dasharray="{lead:.5f} {100-lead:.5f}" opacity=".55">{animation}</rect>'

def strip_motion(text):return re.sub(r'<animate(?:Motion|Transform)?\b[^>]*/>','',text)

def branch_groups(groups,width,y,title,ink,muted,accent,panel,line):
 from vector_logos import logo
 parts=[lettering(title,50,y+17,22,accent,600)]
 columns=min(2 if width==600 else 3,len(groups));cell=(width-80)/columns;top=y+48
 for start in range(0,len(groups),columns):
  row=groups[start:start+columns];offset=(columns-len(row))*cell/2;heights=[];frames=[]
  for col,g in enumerate(row):
   gx=50+offset+col*cell
   parts.append(logo(g['name'],gx+18,top,accent,size=22));parts.append(lettering(g['name'],gx+46,top+18,21,ink,600,max_width=cell-54))
   bx,by=gx+18,top+34;row_height=36
   for label in g['tools']:
    bw=min(measure(label,20)+55,cell-36);lines=[label]
    if measure(label,20)>(bw-45)/.82:
     words=label.split()
     if len(words)>1:
      split=min(range(1,len(words)),key=lambda i:max(measure(' '.join(words[:i]),20),measure(' '.join(words[i:]),20)))
      lines=[' '.join(words[:split]),' '.join(words[split:])]
    bh=56 if len(lines)>1 else 36
    if bx+bw>gx+cell-6:bx=gx+18;by+=row_height+12;row_height=36
    row_height=max(row_height,bh)
    parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="{panel}" stroke="{line}"/>');parts.append(halo(bx,by,bw,bh,accent));parts.append(logo(label,bx+10,by+(bh-18)/2,muted,panel))
    for i,text in enumerate(lines):parts.append(lettering(text,bx+36,by+23+i*21 if len(lines)>1 else by+25,20,ink,550,max_width=bw-45))
    bx+=bw+9
   h=by+row_height+18-top;heights.append(h)
   frames.append(gx)
  for gx in frames:parts.append(f'<path d="M{gx} {top+30}v{max(heights)-30}h{cell-18}" stroke="{line}" fill="none"/>')
  top+=max(heights)+14
 return parts,top+12
