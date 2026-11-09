from pathlib import Path
import re
from build_identity import lettering,font_at

def measure(text,size=20,weight=550):
 f=font_at(weight);c=f.getBestCmap();return sum(f['hmtx'][c.get(ord(ch),'.notdef')][0] for ch in text)*size/f['head'].unitsPerEm

def centered(text,width,y,size,color,weight=550):return lettering(text,(width-measure(text,size,weight))/2,y,size,color,weight)

def halo(x,y,w,h,color,phase=0,still=False):
 if still:return ''
 shape=f'x="{x}" y="{y}" width="{w}" height="{h}" rx="10" pathLength="100" fill="none" stroke="{color}" stroke-width="1"'
 return f'<rect {shape} opacity=".16"/><rect {shape} stroke-dasharray="12 88" opacity=".6"><animate attributeName="stroke-dashoffset" from="{phase}" to="{phase-100}" dur="6s" repeatCount="indefinite"/></rect>'

def strip_motion(text):return re.sub(r'<animate\b[^>]*/>','',text)
