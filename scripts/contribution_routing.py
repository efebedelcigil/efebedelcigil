"""Deterministic package sizing, terminal routing and calendar labels."""
import math,heapq
import pcb_components
from pcb_components import META,body_origin,variant_at,scaled_chip
from build_identity import lettering
def land_bounds(g,cell,level):
 origin=g.package_origin(cell,level);variant=variant_at(*origin,level);k=g.sizes.get(cell,1)
 rx,ry=(1.35,1.35) if level==2 else (1.3,1.1 if level==4 else 2.9)
 if variant>4:rx,ry=ry,rx
 pins=pcb_components.contacts(g.chip,*origin,level);rx*=k;ry*=k
 return min(x for x,y in pins)-rx,min(y for x,y in pins)-ry,max(x for x,y in pins)+rx,max(y for x,y in pins)+ry

def configure_sizes(g,cells,days):
 active={cells[d]:level for d,level in days.items() if level};g.sizes={cell:.6 for cell in active}
 def bounds(cell,level):
  origin=g.package_origin(cell,level);return g.project_package_bounds(origin,level,2.0)
 def overlaps(a,b):return not(a[2]<=b[0] or b[2]<=a[0] or a[3]<=b[1] or b[3]<=a[1])
 boxes={cell:bounds(cell,level) for cell,level in active.items()}
 for step in range(1,22):
  for kind in range(1,5):
   matching=[c for c,v in active.items() if v==kind]
   if not matching:continue
   old={c:g.sizes[c] for c in matching};candidate=.6+step*.05
   for cell in matching:g.sizes[cell]=candidate
   proposed={c:bounds(c,active[c]) for c in matching};combined={**boxes,**proposed};valid=True
   for cell in matching:
    l,t,r,b=land_bounds(g,cell,kind);cx,cy=g.center(cell)
    if min(l-cx+g.step/2,cx+g.step/2-r,t-cy+g.row_pitch/2,cy+g.row_pitch/2-b)<1.5:valid=False;break
    if any(overlaps(proposed[cell],box) for other,box in combined.items() if other!=cell and abs(other[0]-cell[0])<=3 and abs(other[1]-cell[1])<=2):valid=False;break
   if valid:boxes=combined
   else:
    for cell in matching:g.sizes[cell]=old[cell];g.package_origin(cell,kind)
 # A package type has one size across all dates and orientations.
 for level in range(1,5):
  matching=[cell for cell,value in active.items() if value==level]
  if not matching:continue
  size=min(g.sizes[cell] for cell in matching)
  for cell in matching:g.sizes[cell]=size;g.package_origin(cell,level)
 for cell,level in active.items():
  origin=g.package_origin(cell,level);l,t,r,b=land_bounds(g,cell,level);cx,cy=g.center(cell)
  assert min(l-(cx-g.step/2),(cx+g.step/2)-r,t-(cy-g.row_pitch/2),(cy+g.row_pitch/2)-b)>=1.5-1e-6, 'Pad crosses its cell clearance'
 return g.sizes
CACHE={};VALIDATION={}
def physical_route(geometry,cells,days,ring):
 configure_sizes(geometry,cells,days)
 key=tuple(sorted(days.items()))
 if key in CACHE:return CACHE[key]
 chip=geometry.chip;parts={}
 for date,level in days.items():
  if not level:continue
  cell=cells[date];origin=geometry.package_origin(cell,level);pins=pcb_components.contacts(chip,*origin,level)
  # The contact-side corridor sits beyond the package, before the real pad.
  variant=variant_at(*origin,level);body=META['parts'][str(variant)]['body_plane_bounds'];k=geometry.sizes.get(cell,1);sx,sy=chip.width/12*k,chip.height/18*k
  keep=(origin[0]+body[0]*sx-.6,origin[1]+body[1]*sy-.6,origin[0]+body[2]*sx+.6,origin[1]+body[3]*sy+.6)
  parts[cell]={'date':date,'level':level,'variant':variant,'size':k,'origin':origin,'pins':pins,'keep':keep}
 pitch=1.2;blocked=set();nx=math.ceil(geometry.width/pitch);ny=math.ceil(geometry.height/pitch)
 def grid(p):return round(p[0]/pitch),round(p[1]/pitch)
 for part in parts.values():
  l,t,r,b=part['keep']
  for x in range(math.floor(l/pitch),math.ceil(r/pitch)+1):
   for y in range(math.floor(t/pitch),math.ceil(b/pitch)+1):
    if l<=x*pitch<=r and t<=y*pitch<=b:blocked.add((x,y))
 for part in parts.values():
  level=part['level'];rx,ry=(1.7,3.3) if level in [1,3] else ((1.7,1.5) if level==4 else (1.7,1.7))
  rx*=part['size'];ry*=part['size']
  if part['variant']>4:rx,ry=ry,rx
  for px,py in part['pins']:
   for xx in range(math.floor((px-rx)/pitch),math.ceil((px+rx)/pitch)+1):
    for yy in range(math.floor((py-ry)/pitch),math.ceil((py+ry)/pitch)+1):
     if abs(xx*pitch-px)<=rx and abs(yy*pitch-py)<=ry:blocked.add((xx,yy))
 def astar(a,b,use_channel=True):
  if use_channel and abs(a[0]-b[0])>geometry.step*6:
   edge=8 if a[1]+b[1]<geometry.height else geometry.height-8
   first=(a[0],edge);last=(b[0],edge)
   return astar(a,first,False)+[last]+astar(last,b,False)[1:]
  start,end=grid(a),grid(b);q=[(0,0,start)];cost={start:0};parent={};heading={}
  def free(p):return 2<p[0]<nx-2 and 2<p[1]<ny-2 and (p not in blocked or p in [start,end])
  for _ in range(30000):
   if not q:break
   _,g,u=heapq.heappop(q)
   if g>cost[u]+1e-6:continue
   if u==end:
    path=[end]
    while path[-1]!=start:path.append(parent[path[-1]])
    path.reverse();points=[a]+[(x*pitch,y*pitch) for x,y in path[1:-1]]+[b];result=[points[0]]
    for i in range(1,len(points)-1):
     v=(points[i][0]-points[i-1][0],points[i][1]-points[i-1][1]);w=(points[i+1][0]-points[i][0],points[i+1][1]-points[i][1])
     if abs(v[0]*w[1]-v[1]*w[0])>1e-6:result.append(points[i])
    return result+[points[-1]]
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
    v=u[0]+dx,u[1]+dy
    if not free(v) or (dx and dy and (not free((u[0]+dx,u[1])) or not free((u[0],u[1]+dy)))):continue
    ng=g+(1.4142 if dx and dy else 1)+(.7 if u in heading and heading[u]!=(dx,dy) else 0)
    if ng>=cost.get(v,float('inf')):continue
    cost[v]=ng;parent[v]=u;heading[v]=(dx,dy);ax,ay=abs(v[0]-end[0]),abs(v[1]-end[1]);heapq.heappush(q,(ng+max(ax,ay)+.4142*min(ax,ay),ng,v))
  raise RuntimeError(f'Terminal route unavailable: {a} -> {b}')
 def port(part,pin):
  l,t,r,b=part['keep']
  if part['variant']>4:return (pin[0],min(t-.8,pin[1]-2.8*part['size']) if pin[1]<part['origin'][1] else max(b+.8,pin[1]+2.8*part['size']))
  return (min(l-.8,pin[0]-2.8*part['size']) if pin[0]<part['origin'][0] else max(r+.8,pin[0]+2.8*part['size']),pin[1])
 ordered=list(dict.fromkeys(cell for cell in ring if cell in parts));nodes=[];checks=[]
 if not ordered:return [geometry.center(c) for c in ring]+[geometry.center(ring[0])],''
 for i,cell in enumerate(ordered):
  part=parts[cell];before=geometry.center(ordered[(i-1)%len(ordered)]);after=geometry.center(ordered[(i+1)%len(ordered)])
  entry=min(part['pins'],key=lambda p:math.dist(p,before));exit=min((p for p in part['pins'] if p!=entry),key=lambda p:math.dist(p,after));nodes.append((part,entry,exit))
 # Select the pair jointly against actual neighboring terminal ports.
 # Penalize approaches behind the outward terminal normal to avoid hairpins.
 def approach_cost(part,pin,neighbor):
  stub=port(part,pin);vx=stub[0]-pin[0];vy=stub[1]-pin[1]
  nx=neighbor[0]-stub[0];ny=neighbor[1]-stub[1];length=math.hypot(nx,ny)
  cosine=(vx*nx+vy*ny)/max(1e-9,math.hypot(vx,vy)*length)
  return length+5*(1-cosine)
 for sweep in range(3):
  for i,(part,entry,exit) in enumerate(nodes):
   previous,_,previous_exit=nodes[(i-1)%len(nodes)];following,following_entry,_=nodes[(i+1)%len(nodes)]
   before=port(previous,previous_exit);after=port(following,following_entry)
   entry,exit=min(((a,b) for a in part['pins'] for b in part['pins'] if a!=b),key=lambda pair:approach_cost(part,pair[0],before)+approach_cost(part,pair[1],after))
   nodes[i]=(part,entry,exit)
 points=[];corridors=[]
 for i,(part,entry,exit) in enumerate(nodes):
  nextpart,nextentry,_=nodes[(i+1)%len(nodes)]
  points.extend([entry,exit]);outside=astar(port(part,exit),port(nextpart,nextentry));points+=outside;points.append(nextentry)
  corridors.extend([(part,port(part,entry),entry),(part,port(part,exit),exit)])
  checks.append({'date':part['date'],'entry':entry,'exit':exit,'entry_error':math.dist(points[-1],nextentry),'exit_error':math.dist(points[-len(outside)-2],exit)})
 points.append(points[0])
 protected={p for _,entry,exit in nodes for p in [entry,exit]};smoothed=[points[0]]
 for i in range(1,len(points)-1):
  a,b,c=points[i-1],points[i],points[i+1];la=math.dist(a,b);lb=math.dist(b,c)
  if b in protected or min(la,lb)<1e-6:smoothed.append(b);continue
  cross=(b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
  if abs(cross)<1e-6:smoothed.append(b);continue
  cut=min(.9,la*.25,lb*.25);start=(b[0]+(a[0]-b[0])*cut/la,b[1]+(a[1]-b[1])*cut/la);end=(b[0]+(c[0]-b[0])*cut/lb,b[1]+(c[1]-b[1])*cut/lb)
  smoothed.append(start)
  for j in range(1,7):
   t=j/6;smoothed.append(((1-t)**2*start[0]+2*(1-t)*t*b[0]+t*t*end[0],(1-t)**2*start[1]+2*(1-t)*t*b[1]+t*t*end[1]))
 smoothed.append(points[-1]);points=smoothed
 assert protected.issubset(points)
 defs=[];patches=[]
 for index,(part,outside,pin) in enumerate(corridors):
  polygon=' '.join(f'{x},{y}' for x,y in chip.polygon(*part['origin'],part['level']))
  defs.append(f'<clipPath id="terminalClip{index}"><polygon points="{polygon}"/></clipPath>')
  patches.append(f'<g clip-path="url(#terminalClip{index})"><path d="M{outside[0]} {outside[1]}L{pin[0]} {pin[1]}" stroke="white" stroke-width="6.5" stroke-linecap="butt"/></g>')
 data={'clip_defs':''.join(defs),'patches':''.join(patches),'terminal_checks':checks,'parts':parts,'nodes':nodes,'astar':astar,'port':port}
 CACHE[key]=(points,data);return points,data

def calendar_labels(g,cells,days,color):
 import datetime
 from build_identity import lettering
 a,b,c,d=g.projection
 def screen(x,y):return g.tx+(a*x+c*y)*g.scale,g.ty+(b*x+d*y)*g.scale
 parts=[];months=set()
 for date in sorted(days):
  key=date[:7]
  if key in months:continue
  months.add(key);col=cells[date][0];x,y=screen(g.padding+col*g.step,0)
  parts.append(lettering(datetime.date.fromisoformat(date).strftime('%b'),x,y-8,11,color,550))
 for row,label in enumerate(['Su','Mo','Tu','We','Th','Fr','Sa']):
  x,y=screen(0,g.padding+(row+.5)*g.row_pitch)
  parts.append(lettering(label,x-24,y+4,11,color,550))
 return parts
