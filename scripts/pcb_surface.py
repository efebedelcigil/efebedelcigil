"""Lightweight board-surface treatment derived from current package geometry."""
from contribution_routing import land_bounds

def surface_regions(geometry,cells,days):
 regions=[]
 for date,level in sorted(days.items()):
  if not level:continue
  cell=cells[date];l,t,r,b=land_bounds(geometry,cell,level)
  regions.append({'date':date,'ellipse':((l+r)/2,(t+b)/2,(r-l)/2+3,(b-t)/2+2)})
 return regions

def quiet_weight(x,y,regions):
 import math
 distance=min((math.hypot((x-r['ellipse'][0])/(r['ellipse'][2]*1.35),(y-r['ellipse'][1])/(r['ellipse'][3]*1.35)) for r in regions),default=2)
 t=min(1,max(0,distance));return .24+.76*t*t*(3-2*t)

def quiet_trace_paths(paths,regions):
 import math
 buckets={}
 for path in paths:
  for a,b in zip(path,path[1:]):
   near=any(min(a[0],b[0])<=r['ellipse'][0]+r['ellipse'][2]*1.35 and max(a[0],b[0])>=r['ellipse'][0]-r['ellipse'][2]*1.35 and min(a[1],b[1])<=r['ellipse'][1]+r['ellipse'][3]*1.35 and max(a[1],b[1])>=r['ellipse'][1]-r['ellipse'][3]*1.35 for r in regions)
   count=max(1,math.ceil(math.dist(a,b)/5)) if near else 1
   for i in range(count):
    t0=i/count;t1=(i+1)/count;x0=a[0]+(b[0]-a[0])*t0;y0=a[1]+(b[1]-a[1])*t0;x1=a[0]+(b[0]-a[0])*t1;y1=a[1]+(b[1]-a[1])*t1
    weight=round(quiet_weight((x0+x1)/2,(y0+y1)/2,regions)*8)/8
    buckets.setdefault(weight,[]).append(f'M{x0:.2f} {y0:.2f}L{x1:.2f} {y1:.2f}')
 return ''.join(f'<path data-trace-weight="{weight}" opacity="{weight}" d="'+''.join(parts)+'"/>' for weight,parts in sorted(buckets.items()))

def surface_art(geometry,cells,days,theme):
 regions=surface_regions(geometry,cells,days);color='#071c13' if theme=='dark' else '#173c29'
 definitions=f'<defs><radialGradient id="pcbContactShade"><stop stop-color="{color}" stop-opacity=".48"/><stop offset=".45" stop-color="{color}" stop-opacity=".22"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient></defs>'
 shadows=['<g data-contact-shadows="true">']
 for region in regions:
  x,y,rx,ry=region['ellipse']
  shadows.append(f'<ellipse data-trace-quiet="{region["date"]}" data-contact-shadow="{region["date"]}" cx="{x+.6}" cy="{y+.8}" rx="{rx}" ry="{ry}" fill="url(#pcbContactShade)"/>')
 shadows.append('</g>');return definitions,''.join(shadows)
