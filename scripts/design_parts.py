from labels import display_label
from pathlib import Path
import re
from build_identity import lettering,font_at

def measure(text,size=20,weight=550):
 text=display_label(text)
 f=font_at(weight);c=f.getBestCmap();return sum(f['hmtx'][c.get(ord(ch),'.notdef')][0] for ch in text)*size/f['head'].unitsPerEm

def centered(text,width,y,size,color,weight=550):return lettering(text,(width-measure(text,size,weight))/2,y,size,color,weight)

def electric_trace(path,color,weight=1.4,electric=True):
 animation='<animate attributeName="stroke-dashoffset" from="0" to="-100" begin="0s" dur="8s" repeatCount="indefinite"/>'
 shape=f'd="{path}" pathLength="100" fill="none" stroke="{color}" stroke-linecap="round" stroke-linejoin="round"'
 result=f'<g data-halo="true">{animation}<path {shape} stroke-width="{weight+2.5}" stroke-dasharray="18 82" opacity=".07"/><path {shape} stroke-width="{weight}" stroke-dasharray="25 75" opacity=".23"/><path {shape} stroke-width="{weight}" stroke-dasharray="8 92" opacity=".85"/></g>'
 if electric:
  result+=f'<g data-border-current="true" fill="none" stroke="{color}" stroke-width=".8" stroke-linecap="round" opacity=".5"><path d="M-3 0l2 -1 1 2 2 -1m-1 -2l1 -1 1 1"><animate attributeName="opacity" values=".3;.8;.4;.7;.3" dur="1.3s" repeatCount="indefinite"/></path><animateMotion path="{path}" begin="-.32s" dur="8s" rotate="auto" repeatCount="indefinite"/></g>'
 return result

def halo(x,y,w,h,color,still=False,radius=10,weight=1.4,electric=True):
 if still:return ''
 r=min(radius,w/2,h/2)
 path=f'M{x+w/2} {y}H{x+w-r}Q{x+w} {y} {x+w} {y+r}V{y+h-r}Q{x+w} {y+h} {x+w-r} {y+h}H{x+r}Q{x} {y+h} {x} {y+h-r}V{y+r}Q{x} {y} {x+r} {y}Z'
 return electric_trace(path,color,weight,electric)

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
