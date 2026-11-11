"""Seeded chamfered PCB nets, independent of the calendar grid."""
import random,math

def distance(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy or 1)))
 return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)

def crosses(a,b,c,d):
 def turn(p,q,r):return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
 return turn(a,b,c)*turn(a,b,d)<0 and turn(c,d,a)*turn(c,d,b)<0

from functools import lru_cache
import heapq

@lru_cache(maxsize=8)
def tracks(width,height,padding=18):
 rng=random.Random(43019);routes=[];segments=[];vias=[];occupied=set();raw_routes=[];pitch=2.2;coverage=[0]*18
 cols=int((width-2*padding)/pitch);rows=int((height-2*padding)/pitch)
 directions=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
 def free(p):return 0<=p[0]<=cols and 0<=p[1]<=rows and p not in occupied
 def world(p):return padding+p[0]*pitch,padding+p[1]*pitch
 def heuristic(p,b):
  dx,dy=abs(p[0]-b[0]),abs(p[1]-b[1]);return max(dx,dy)+.41421356*min(dx,dy)
 for attempt in range(330):
  if raw_routes and rng.random()<.35:
   old=rng.choice(raw_routes);ox,oy=rng.choice([(2,0),(0,2),(-2,0),(0,-2),(3,0),(0,3)])
   a=(old[0][0]+ox,old[0][1]+oy);b=(old[-1][0]+ox,old[-1][1]+oy)
  else:
   region=min(rng.sample(range(18),6),key=lambda i:coverage[i]);rx=region%6;ry=region//6
   a=(min(cols,int((rx+rng.random())*cols/6)),min(rows,int((ry+rng.random())*rows/3)));b=(max(0,min(cols,a[0]+rng.randint(-90,90))),max(0,min(rows,a[1]+rng.randint(-35,35))))
  if not free(a) or not free(b) or heuristic(a,b)<12:continue
  queue=[(heuristic(a,b),0,a)];cost={a:0};parent={};heading={};found=False
  for _ in range(3500):
   if not queue:break
   _,g,u=heapq.heappop(queue)
   if g>cost[u]+1e-8:continue
   if u==b:found=True;break
   for direction,(dx,dy) in enumerate(directions):
    v=(u[0]+dx,u[1]+dy)
    if not free(v) or (dx and dy and (not free((u[0]+dx,u[1])) or not free((u[0],u[1]+dy)))):continue
    ng=g+(1.41421356 if dx and dy else 1)+(.9 if u in heading and heading[u]!=direction else 0)
    if ng>=cost.get(v,float('inf')):continue
    cost[v]=ng;parent[v]=u;heading[v]=direction;heapq.heappush(queue,(ng+heuristic(v,b),ng,v))
  if not found:continue
  cells=[b]
  while cells[-1]!=a:cells.append(parent[cells[-1]])
  cells.reverse();reduced=[cells[0]]
  for i in range(1,len(cells)-1):
   if (cells[i][0]-cells[i-1][0],cells[i][1]-cells[i-1][1])!=(cells[i+1][0]-cells[i][0],cells[i+1][1]-cells[i][1]):reduced.append(cells[i])
  reduced.append(cells[-1]);points=list(map(world,reduced));new=list(zip(points,points[1:]))
  if any(crosses(u,v,s,t) or min(distance(u,s,t),distance(v,s,t),distance(s,u,v),distance(t,u,v))<3.9 for u,v in new for s,t in segments):continue
  if any(math.dist(p,q)<5.2 for p in [points[0],points[-1]] for q in vias):continue
  routes.append(points);segments+=new;vias.extend([points[0],points[-1]]);raw_routes.append(cells)
  for x,y in cells:
   coverage[min(5,int(x/max(cols,1)*6))+6*min(2,int(y/max(rows,1)*3))]+=1
   for dx in [-1,0,1]:
    for dy in [-1,0,1]:occupied.add((x+dx,y+dy))
  if len(routes)==85:break
 return routes,vias
