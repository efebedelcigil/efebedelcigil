"""Shared package geometry, perspective clearance and board fitting."""
from dataclasses import dataclass
from pcb_components import META,body_origin,ORIENTATIONS,SCALES,PAD_TURNS,scaled_chip,variant_at
from dataclasses import replace

@dataclass(frozen=True)
class ChipGeometry:
 width: float=12
 height: float=18
 lift_base: float=.8
 lift_step: float=.7
 def __post_init__(self):
  if self.width<=6 or self.height<=4 or self.lift_base<0 or self.lift_step<0:raise ValueError('Invalid package dimensions')
 def lift(self,level):return self.lift_base+self.lift_step*level
 def polygon(self,x,y,level):
  original_level=level;self_scaled=scaled_chip(self,x,y,level);level=variant_at(x,y,level)
  points=META['parts'][str(level)]['polygon'] if level else [(-8,-1.5),(-8,1.5),(8,-1.5),(8,1.5)]
  sx,sy=self_scaled.width/12,self_scaled.height/18
  return [(x+px*sx,y+py*sy) for px,py in points]
 def bounds(self,x,y,level):
  points=self.polygon(x,y,level)
  return min(x for x,y in points),min(y for x,y in points),max(x for x,y in points),max(y for x,y in points)

class BoardGeometry:
 def __init__(self,weeks,projection=None,chip=ChipGeometry(),rows=7):
  self.weeks=weeks;self.rows=rows;self.chip=chip
  if projection is None:
   aa,cc,bb,dd=META['projection'];projection=(aa,bb,cc,dd)
  self.projection=projection
  a,b,c,d=projection
  if abs(a*d-b*c)<1e-5:raise ValueError('Degenerate board perspective')
  boxes=[self.project_package_bounds(body_origin(chip,level),level) for level in range(9)]
  w=max(box[2] for box in boxes)-min(box[0] for box in boxes)+.6;h=max(box[3] for box in boxes)-min(box[1] for box in boxes)+.6
  self.step=(w+2.4)/max(abs(a),.1);self.row_pitch=h/max(abs(d),.1)*1.7
  for attempt in range(160):
   overlap=any(abs(a*col*self.step+c*row*self.row_pitch)<w and abs(b*col*self.step+d*row*self.row_pitch)<h for col in range(1-weeks,weeks) for row in range(1-rows,rows) if col or row)
   if not overlap:break
   self.step*=1.04;self.row_pitch*=1.04
  else:raise ValueError('Unable to separate projected packages')
  self.padding=18
  self.width=self.step*weeks+2*self.padding;self.height=rows*self.row_pitch+2*self.padding
  left,top,right,bottom=self.project_bounds((0,0,self.width,self.height+10))
  self.scale=min(1,1040/(right-left),380/(bottom-top))
  if min(chip.width,chip.height)*self.scale<4:raise ValueError('Perspective makes packages unreadable')
  tx=40+(1040-(right-left)*self.scale)/2-left*self.scale
  ty=80-top*self.scale
  self.screen_bottom=ty+bottom*self.scale;self.tx=tx;self.ty=ty
  self.transform=f'translate({tx} {ty}) matrix({a} {b} {c} {d} 0 0) scale({self.scale})'
 def project(self,x,y):
  a,b,c,d=self.projection;return a*x+c*y,b*x+d*y
 def project_bounds(self,bounds,padding=0):
  left,top,right,bottom=bounds;points=[self.project(x,y) for x in [left,right] for y in [top,bottom]]
  return min(x for x,y in points)-padding,min(y for x,y in points)-padding,max(x for x,y in points)+padding,max(y for x,y in points)+padding
 def origin(self,cell):
  x,y=self.center(cell);return x-self.chip.width/2,y-self.chip.height/2
 def center(self,cell):
  return self.padding+(cell[0]+.5)*self.step,self.padding+(cell[1]+.5)*self.row_pitch
 def package_origin(self,cell,level):
  x,y=self.center(cell);variant=level+4 if level and (cell[0]*17+cell[1]*11)%7<3 else level;k=getattr(self,"sizes",{}).get(cell,1);dx,dy=body_origin(replace(self.chip,width=self.chip.width*k,height=self.chip.height*k),variant)
  offset=((cell[0]*7+cell[1]*3+level*2)%5-2)*.15 if level else 0
  origin=(x+dx,y+dy+offset)
  ORIENTATIONS[(round(origin[0],6),round(origin[1],6),level)]=variant
  SCALES[(round(origin[0],6),round(origin[1],6),level)]=k
  if not level:PAD_TURNS[(round(origin[0],6),round(origin[1],6))]=90 if (cell[0]*17+cell[1]*11)%7<3 else 0
  return origin

 def project_package_bounds(self,origin,level,padding=0):
  points=[self.project(x,y) for x,y in self.chip.polygon(*origin,level)]
  return min(x for x,y in points)-padding,min(y for x,y in points)-padding,max(x for x,y in points)+padding,max(y for x,y in points)+padding
 def occluder(self,cell,level,padding=3):return self.project_package_bounds(self.package_origin(cell,level),level,padding)
 def mounts(self):return [(x,y) for x in [14,self.width-14] for y in [14,self.height-14]]
