"""Small reusable profile visuals."""
import contribution_geometry as mod
from pcb_components import META,empty_lands
def legend_sprite(level,cx,cy,k):
 if not level:
  lands=empty_lands(mod.ChipGeometry(),0,0,0,'none','#c0c8bc','#897553')
  a,b,c,d=mod.META['projection']
  return f'<g data-legend-pads="true" transform="translate({cx} {cy}) scale({k}) matrix({a} {c} {b} {d} 0 0)">'+lands+'</g>'
 w,h=META['parts'][str(level)]['image'][2:]
 return f'<use data-legend-part="{level}" href="#physicalPart{level}" x="{cx-w*k/2}" y="{cy-h*k/2}" width="{w*k}" height="{h*k}" preserveAspectRatio="xMidYMid meet"/>'
def click_cursor(x,y,color,panel):
 hand='M10 26V7C10 2 17 2 17 7V20V17C17 12 24 12 24 17V21V20C24 15 31 15 31 20V23C31 19 38 19 38 24V33C38 40 33 45 27 47H19C15 45 12 41 9 37L3 29C0 25 5 21 8 25L10 28Z'
 return f'''<g data-click-cursor="true" transform="translate({x} {y})" stroke="{color}" stroke-linecap="round" stroke-linejoin="round">
 <g data-click-press="true"><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 1.5;0 0;0 0" keyTimes="0;.45;.49;.54;1" dur="8s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1"/>
 <path d="{hand}" fill="{panel}" stroke-width="2.1"/>
</g>
 <g fill="none" stroke-width="1.6" opacity=".3"><path d="M13 -3V-8M5 1L1 -3M22 1L26 -3"/><animate attributeName="opacity" values=".3;.3;.8;.3;.3" keyTimes="0;.45;.49;.55;1" dur="8s" repeatCount="indefinite"/></g>
 <circle cx="13.5" cy="5" r="3" fill="none" stroke-width="1.3" opacity="0"><animate attributeName="r" values="3;3;8;8;3" keyTimes="0;.45;.55;.56;1" dur="8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0;.45;0;0" keyTimes="0;.45;.49;.56;1" dur="8s" repeatCount="indefinite"/></circle></g>'''
