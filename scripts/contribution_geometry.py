"""Shared package geometry, perspective clearance and board fitting."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ChipGeometry:
 width: float=12
 height: float=13
 lift_base: float=2
 lift_step: float=2
 def __post_init__(self):
  if self.width<=6 or self.height<=4 or self.lift_base<0 or self.lift_step<0:raise ValueError('Invalid package dimensions')
 def lift(self,level):return self.lift_base+self.lift_step*level
 def bounds(self,x,y,level):return x-1,y-self.lift(level),x+self.width+2,y+self.height+3

class BoardGeometry:
 def __init__(self,weeks,projection=(1,.025,-.1,.94),chip=ChipGeometry(),rows=7):
  self.weeks=weeks;self.rows=rows;self.projection=projection;self.chip=chip
  a,b,c,d=projection
  if abs(a*d-b*c)<1e-5:raise ValueError('Degenerate board perspective')
  self.step=948/max(weeks-1,1);self.row_pitch=chip.height+chip.lift(4)+7
  box=self.project_bounds(chip.bounds(0,0,4));w=box[2]-box[0]+.25;h=box[3]-box[1]+.25
  for attempt in range(160):
   overlap=any(abs(a*col*self.step+c*row*self.row_pitch)<w and abs(b*col*self.step+d*row*self.row_pitch)<h for col in range(1-weeks,weeks) for row in range(1-rows,rows) if col or row)
   if not overlap:break
   self.step*=1.04;self.row_pitch*=1.04
  else:raise ValueError('Unable to separate projected packages')
  self.width=self.step*max(weeks-1,1)+62;self.height=rows*self.row_pitch+36
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
 def origin(self,cell):return 20+cell[0]*self.step,20+cell[1]*self.row_pitch
 def center(self,cell):
  x,y=self.origin(cell);return x+self.chip.width/2,y+self.chip.height/2
 def occluder(self,cell,level,padding=3):return self.project_bounds(self.chip.bounds(*self.origin(cell),level),padding)
