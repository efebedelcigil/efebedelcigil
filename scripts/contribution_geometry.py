"""Shared package geometry, perspective clearance and board fitting."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ChipGeometry:
 width: float=8
 height: float=14
 lift_base: float=.8
 lift_step: float=.7
 def __post_init__(self):
  if self.width<=6 or self.height<=4 or self.lift_base<0 or self.lift_step<0:raise ValueError('Invalid package dimensions')
 def lift(self,level):return self.lift_base+self.lift_step*level
 def bounds(self,x,y,level):
  mid=y+self.height/2
  if level==0:return x-4.5,mid-1.5,x+self.width+4.5,mid+1.5
  if level==1:return x-4.5,mid-3,x+self.width+4.5,mid+3
  if level==2:return x-3.5,mid-10,x+self.width+2,mid+8
  if level==3:return x-4.5,mid-6,x+self.width+4.5,mid+7
  return x-4.5,y-self.lift(level),x+self.width+4.5,y+self.height+3

class BoardGeometry:
 def __init__(self,weeks,projection=(1,.10,-.24,.88),chip=ChipGeometry(),rows=7):
  self.weeks=weeks;self.rows=rows;self.projection=projection;self.chip=chip
  a,b,c,d=projection
  if abs(a*d-b*c)<1e-5:raise ValueError('Degenerate board perspective')
  self.step=948/max(weeks-1,1);self.row_pitch=chip.height+chip.lift(4)+7
  boxes=[self.project_bounds(chip.bounds(0,0,level)) for level in range(5)]
  w=max(box[2]-box[0] for box in boxes)+.25;h=max(box[3]-box[1] for box in boxes)+.25
  for attempt in range(160):
   overlap=any(abs(a*col*self.step+c*row*self.row_pitch)<w and abs(b*col*self.step+d*row*self.row_pitch)<h for col in range(1-weeks,weeks) for row in range(1-rows,rows) if col or row)
   if not overlap:break
   self.step*=1.04;self.row_pitch*=1.04
  else:raise ValueError('Unable to separate projected packages')
  self.padding=18
  self.width=self.step*weeks+2*self.padding;self.height=rows*self.row_pitch+2*self.padding
  left,top,right,bottom=self.project_bounds((0,0,self.width,self.height+10))
  self.scale=min(1,1040/(right-left),260/(bottom-top))
  if min(chip.width,chip.height)*self.scale<4:raise ValueError('Perspective makes packages unreadable')
  tx=40+(1040-(right-left)*self.scale)/2-left*self.scale
  ty=80+(260-(bottom-top)*self.scale)/2-top*self.scale
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
  x,y=self.center(cell);left,top,right,bottom=self.chip.bounds(0,0,level)
  return x-(left+right)/2,y-(top+bottom)/2
 def occluder(self,cell,level,padding=3):return self.project_bounds(self.chip.bounds(*self.package_origin(cell,level),level),padding)
 def mounts(self):return [(x,y) for x in [14,self.width-14] for y in [14,self.height-14]]
