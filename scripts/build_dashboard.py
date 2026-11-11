from labels import display_label
from pathlib import Path
import json,html,re,xml.etree.ElementTree as E,datetime
from build_identity import lettering
from circuit_route import circuit_route,spark_gate
from contribution_geometry import BoardGeometry
from pcb_components import KINDS,component,pads,definitions
from pcb_background import tracks
from public_calendar import cell_map
from design_parts import halo,electric_trace,centered,measure,strip_motion,branch_groups
R=Path(__file__).resolve().parents[1];A=R/'assets'
profile=json.loads((A/'profile.json').read_text(encoding='utf-8'));public=json.loads((A/'public-profile.json').read_text(encoding='utf-8'))
from vector_logos import logo
for theme in ('dark','light'):
 ink,muted,blue,copper,panel,line=('#edf2f8','#a9b8cc','#78a4ff','#efa571','#142237','#31445e') if theme=='dark' else ('#25394d','#53677d','#365d94','#925c3c','#e4ebf1','#bdcbd9')
 def txt(t,x,y,s=22,c=None,w=550):return lettering(t,x,y,s,c or ink,w)
 def save(name,w,h,p):
  if name.startswith('heading-'):
   seed=sum(map(ord,name));length=48+(seed%4)*17
   decoration=f'<g fill="none" stroke="{blue}" stroke-width=".8" opacity=".46"><path d="M12 6h{length*.6}l8 8h{length*.3}m{-length*.5} -11h{length*.3}l8 8M{w-15} 6h{-length*.7}l-7 7h{-length*.2}m30 -10h-18l-7 7M{24+seed%30} 42h24l8 -8h16"/><circle cx="12" cy="6" r="1.5"/><circle cx="{w-15}" cy="6" r="1.5"/></g>'
   p=[decoration]+p
  (A/f'{name}-{theme}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{html.escape(name)}</title>'+''.join(p)+'</svg>',encoding='utf-8')
  path=A/f'{name}-{theme}.svg'
  if '<animate' in path.read_text(encoding='utf-8'):
   (A/f'{name}-{theme}-still.svg').write_text(strip_motion(path.read_text(encoding='utf-8')),encoding='utf-8')
 def traces(w,y):return f'<path d="M{w-160} {y}h60l20 20h65m-125-9h43l20 20h62" stroke="{line}" fill="none"/><circle cx="{w-15}" cy="{y+20}" r="3" fill="{copper}"/>'
 for mobile in (False,True):
  w=600 if mobile else 1120;suffix='-mobile' if mobile else ''
  support=[[]];row_width=0
  for field in profile['areas'][2:]:
   needed=measure(field,21)+47
   if row_width+needed>w-(60 if mobile else 150):support.append([]);row_width=0
   support[-1].append(field);row_width+=needed
  height=113+(len(support)-1)*39
  p=[f'<rect x="8" y="8" width="{w-16}" height="{height}" rx="14" fill="{panel}" stroke="{line}"/>']
  for i in range(4):p.append(f'<path d="M{w-140+i*18} 19v12l16 16v{height-40}" stroke="{line}" fill="none" opacity=".5"/>')
  title=' & '.join(profile['areas'][:2]);tw=measure(title,32,650)
  p+=[centered(title,w,58,32,blue,650),logo('Control systems',(w-tw)/2-34,34,blue,size=23),logo('Robotics',(w+tw)/2+12,34,blue,size=23)]
  for j,row in enumerate(support):
   widths=[measure(label,21)+33 for label in row];x=(w-sum(widths)-14*(len(row)-1))/2;y=99+j*39
   for label,bw in zip(row,widths):p+=[logo(label,x,y-17,muted),txt(label,x+26,y,21,muted)];x+=bw+14
  p.append('<g opacity=".4">'+electric_trace(f'M{w-121} 19v12l16 16v{height-40}',copper,1)+'</g>')
  p.append(halo(8,8,w-16,height,blue,radius=14))
  save('focus'+suffix,w,height+12,p)
  for name,title,area_key in [('learning','In progress','learning_areas'),('exploring','Interested in exploring','exploring_areas')]:
   p=[];y=16;groups=json.loads((A/(name+'.json')).read_text(encoding='utf-8'))
   area_groups=profile['learning_area_groups' if name=='learning' else 'exploring_area_groups']
   parts,y2=branch_groups(area_groups,w,y,'Areas',ink,muted,copper,panel,line);p+=parts
   parts,end=branch_groups(groups,w,y2,'Tools & methods',ink,muted,blue,panel,line);p+=parts
   save(name+suffix,w,end,p)
  from fontTools.pens.boundsPen import BoundsPen
  from build_identity import font_at
  def extent(text,size,weight):
   text=display_label(text)
   f=font_at(weight);glyphs=f.getGlyphSet();cmap=f.getBestCmap();bounds=[]
   for char in text:
    pen=BoundsPen(glyphs);glyphs[cmap.get(ord(char),'.notdef')].draw(pen)
    if pen.bounds:bounds.append(pen.bounds)
   scale=size/f['head'].unitsPerEm
   return min(b[1] for b in bounds)*scale,max(b[3] for b in bounds)*scale
  title='Explore my portfolio';subtitles=['ALL projects, publications, contact info. and more']
  low,high=extent(title,33,650);sub_low,sub_high=extent(subtitles[-1],21,550)
  shift=98-((60-high)+(100+29*(len(subtitles)-1)-sub_low))/2
  p=[f'<rect x="8" y="8" width="{w-16}" height="180" rx="10" fill="{panel}" stroke="{line}" stroke-width=".5"/>',txt(title,26,60+shift,33,blue,650),*[lettering(text,26,100+i*29+shift,21,muted,550,max_width=w-110) for i,text in enumerate(subtitles)],logo('Open link',w-68,83,copper,size=30)]
  p.append(halo(8,8,w-16,180,'#ffad4d' if theme=='dark' else '#ce6a13',weight=3))
  save('portfolio'+suffix,w,196,p)
 for key,title in [('working','Working areas'),('tools','Tools'),('learning','In progress'),('exploring','Interested in exploring'),('contribution','Contribution circuit'),('languages','Project languages'),('pinned','Pinned repositories')]:
  tw=measure(title,32,650);left=(1120-tw)/2
  p=[centered(title,1120,41,32,blue,650),f'<path d="M40 31H{left-28}m{tw+56} 0H1080" stroke="{blue}" opacity=".6"/><circle cx="{left-16}" cy="31" r="3" fill="{copper}"/>']
  p.append(f'<circle cx="{1120-left+16}" cy="31" r="3" fill="{copper}"/>')
  save('heading-'+key,1120,49,p)
 for name,label in [('github','GitHub'),('linkedin','LinkedIn')]:
  icon=logo(label,12,17,ink,panel)
  save('social-'+name,180,52,[f'<rect x="3" y="3" width="174" height="46" rx="12" fill="{panel}" stroke="{line}"/>',icon,txt(label,41,34,23),logo('Open link',148,18,muted,size=16),halo(3,3,174,46,blue,radius=12)])
 # Pseudo-isometric contribution board: date-to-cell mapping stays identical across themes.
 dates=sorted(public['days']);cells,weeks=cell_map(public['days']);geometry=BoardGeometry(weeks);chip=geometry.chip;cw,ch=chip.width,chip.height;step=geometry.step;pitch=geometry.row_pitch;palette=['none']+['#202b34']*4 if theme=='dark' else ['none']+['#2d3d4c']*4
 panel,line=('#163f30','#315d45') if theme=='dark' else ('#427154','#30563d')
 copper='#cba56f' if theme=='dark' else '#efd4a1'
 metal='#b9c6bd' if theme=='dark' else '#d0d6c9'
 if theme=='light':muted='#53677d'
 period=datetime.date.fromisoformat(dates[0]).strftime('%b %Y')+' / '+datetime.date.fromisoformat(dates[-1]).strftime('%b %Y')
 p=[definitions(),centered(str(sum(public['day_counts'].values()))+' public contributions',1120,26,22,blue,600),centered(period,1120,51,17,muted)]
 p.append(f'<g transform="{geometry.transform}"><rect x="0" y="5.5" width="{geometry.width}" height="{geometry.height}" rx="18" fill="{line}"/>')
 edge_y=geometry.height;edge_x=geometry.width*.43;edge_w=geometry.width*.12
 p.append(f'<path d="M18 {edge_y+2.6}H{geometry.width-18}" stroke="{copper}" stroke-width=".5" opacity=".3"/><path data-cutaway="true" d="M{edge_x} {edge_y+1.5}h{edge_w}m{-edge_w} 2.5h{edge_w}" stroke="{copper}" stroke-width=".5" opacity=".5"/>')
 for i,(start,end) in enumerate([(0,5.5),(0,2.7),(1.5,4),(0,5.5)]):
  vx=edge_x+(i+1)*edge_w/5
  p.append(f'<path data-edge-via="true" d="M{vx-.7} {edge_y+start}v{end-start}m1.4 0v{start-end}" fill="none" stroke="{copper}" stroke-width=".6" opacity=".7"/>')
 p.append(f'<rect width="{geometry.width}" height="{geometry.height}" rx="18" fill="{panel}" stroke="{muted}" stroke-width=".7"/>')
 p.append(halo(0,0,geometry.width,geometry.height,copper,radius=18,weight=2.1,electric=False))
 # Silkscreen and copper stay in the clear perimeter, outside every day cell.
 for x,y in geometry.mounts():p.append(f'<circle data-mount="true" cx="{x}" cy="{y}" r="3.2" fill="{line}" stroke="{copper}" stroke-width="1"/><circle cx="{x}" cy="{y}" r="1.7" fill="{panel}"/>')
 copper_routes,vias=tracks(geometry.width,geometry.height)
 p.append(f'<g data-board-traces="true" fill="none" stroke="{copper}" stroke-width=".9" opacity=".52">')
 for path in copper_routes:p.append('<path d="M'+' L'.join(f'{x},{y}' for x,y in path)+'"/>')
 for x,y in vias:p.append(f'<circle data-via="true" cx="{x}" cy="{y}" r="1.8" fill="{panel}"/><circle cx="{x}" cy="{y}" r=".75" fill="{line}" stroke="none"/>')
 p.append('</g>')
 for week in range(weeks+1):p.append(f'<path data-grid="vertical" d="M{geometry.padding+week*step} {geometry.padding}v{7*pitch}" stroke="{line}" stroke-width=".6" opacity=".12"/>')
 for row in range(8):p.append(f'<path data-grid="horizontal" d="M{geometry.padding} {geometry.padding+row*pitch}h{weeks*step}" stroke="{line}" stroke-width=".6" opacity=".12"/>')
 chip_start=len(p);empty_pads=[]
 for d in dates:
  cell=cells[d];level=public['days'][d];x,y=geometry.package_origin(cell,level)
  left,top,right,bottom=chip.bounds(x,y,level)
  marker=f'<rect data-date="{d}" data-level="{level}" data-component="{KINDS[level]}" x="{left}" y="{top}" width="{right-left}" height="{bottom-top}" fill="none" opacity="0"><title>{d}: {public["day_counts"][d]} public contributions, level {level}, {KINDS[level]}</title></rect>'
  silk='#afbaa5' if theme=='dark' else '#e0e5cf'
  fx,fy=geometry.center(cell);fw=step*.72;fh=pitch*.68
  empty_pads.append(f'<path data-silkscreen="{d}" d="M{fx-fw/2+3} {fy-fh/2}h-3v3m0 {fh-6}v3h3m{fw-6} 0h3v-3m0 {-fh+6}v-3h-3" fill="none" stroke="{silk}" stroke-width=".55" opacity=".32"/>')
  if not level:
   empty_pads.append(marker+pads(chip,x,y,level,panel,metal,copper));continue
  p.append(marker+pads(chip,x,y,level,panel,metal,copper)+component(chip,x,y,level,panel,metal,copper,ink))
 packages=p[chip_start:];p=p[:chip_start]+empty_pads
 active={cells[d] for d in dates if public['days'][d]}
 route=circuit_route(active,width=weeks)
 levels={cells[d]:public['days'][d] for d in dates}
 points=[geometry.center(cell) for cell in route]
 wire='M'+' L'.join(f'{x},{y}' for x,y in points)
 p.append(f'<path d="{wire}" fill="none" stroke="{copper}" stroke-width="1" opacity=".18"/>')
 p.append(f'<defs><filter id="currentGlow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2"/></filter></defs>')
 for color,weight,blur in [(copper,6,' filter="url(#currentGlow)"'),(copper,2.5,''),('#ffe1bd',.75,'')]:
  p.append(f'<path d="{wire}" pathLength="1000" fill="none" stroke="{color}" stroke-width="{weight}" stroke-dasharray="18 982" stroke-linecap="round"{blur}><animate attributeName="stroke-dashoffset" from="0" to="-1000" dur="14s" repeatCount="indefinite"/></path>')
 if len(points)>1:
  occluders=[geometry.occluder(cell,levels[cell]) for cell in active]
  gate=spark_gate(points,occluders,fade=5,projection=geometry.projection)
  values=';'.join(f'{v:.4f}' for t,v in gate);times=';'.join(f'{t:.7f}' for t,v in gate)
  p.append(f'<g data-current-sparks="true" opacity="0"><animate attributeName="opacity" values="{values}" keyTimes="{times}" dur="14s" begin="-.126s" repeatCount="indefinite"/><g fill="none" stroke="{copper}" stroke-width=".8" stroke-linecap="round" stroke-linejoin="round">')
  rays=[('M-1 -2l-2 -2 1 -1 -2 -2','M-1 -2l-3 -1 2 -2 -2 -2','.67s','0s'),('M2 0l3 -1 -1 -2 2 -1','M2 0l2 -2 1 1 1 -3','.83s','-.19s'),('M0 2l-1 2 2 1 -1 2','M0 2l1 2 -2 1 1 2','1.07s','-.43s')]
  for shape,alternate,duration,begin in rays:
   p.append(f'<path d="{shape}" opacity=".3"><animate attributeName="opacity" values=".28;.75;.35;.65;.2;.28" keyTimes="0;.12;.29;.46;.71;1" dur="{duration}" begin="{begin}" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1" repeatCount="indefinite"/><animate attributeName="d" values="{shape};{alternate};{shape}" dur="{duration}" begin="{begin}" repeatCount="indefinite"/></path>')
  p.append(f'<animateMotion path="{wire}" dur="14s" begin="-.126s" rotate="auto" repeatCount="indefinite"/></g></g>')
 p+=packages
 p.append('</g>')
 legend_scale=.8;gap=12;sample_widths=[]
 for level in range(5):
  if level:
   from pcb_components import META
   width=META['parts'][str(level)]['image'][2]*legend_scale
  else:width=22*legend_scale
  sample_widths.append(width)
 total_width=measure('Less',15)+measure('More',15)+sum(sample_widths)+gap*6
 cursor=(1120-total_width)/2
 p.append(txt('Less',cursor,382,15,muted));cursor+=measure('Less',15)+gap
 for level,width in enumerate(sample_widths):
  left,top,right,bottom=chip.bounds(0,0,level);x=-(left+right)/2;y=-(top+bottom)/2
  p.append(f'<g transform="translate({cursor+width/2} 377) scale({legend_scale})">'+pads(chip,x,y,level,panel,metal,copper)+component(chip,x,y,level,panel,metal,copper,ink)+'</g>')
  cursor+=width+gap
 p.append(txt('More',cursor,382,15,muted))
 save('contribution',1120,410,p)
 save('contribution-still',1120,410,[strip_motion(part) for part in p])
 panel,line,muted=('#142237','#31445e','#a9b8cc') if theme=='dark' else ('#e4ebf1','#bdcbd9','#53677d')
 copper='#efa571' if theme=='dark' else '#925c3c'
 activity=public.get('activity',{})
 p=[centered('Public activity',1120,25,21,copper,600)]
 for i,(label,count) in enumerate(activity.items()):
  display='Repository' if label=='Repositories' and count==1 else label
  text=str(count)+' '+display;size=19 if len(activity)>4 else 21;tw=measure(text,size)+26;cx=(i+.5)*1120/len(activity);x=cx-tw/2
  p.append(logo(label,x,54,blue,size=19));p.append(txt(text,x+26,73,size,ink))
 save('activity',1120,96,p)
 # Language distribution uses public repository language bytes, excluding forks and the profile repository.
 repos=public['repos'];projects=public.get('pinned',[])
 languages=public.get('languages',{});total=sum(languages.values()) or 1
 colors=[blue,copper,'#65b8ae','#a995d0','#aab8c8']
 p=[centered('Public source code / language bytes',1120,25,19,muted)]
 ordered=sorted(languages.items(),key=lambda item:-item[1])
 labels=[language+' '+str(round(value/total*100,1))+'%' for language,value in ordered]
 col_widths=[max([measure(labels[i],20)+19 for i in range(col,len(labels),3)] or [0]) for col in range(3)]
 legend_left=(1120-sum(col_widths)-144)/2
 cursor=8
 for i,(language,value) in enumerate(sorted(languages.items(),key=lambda x:-x[1])):
  span=1104*value/total;c=colors[i%len(colors)]
  p.append(f'<rect x="{cursor}" y="46" width="{span}" height="22" fill="{c}"/>')
  p.append(f'<path d="M{cursor} 41v32" stroke="{line}"/>');cursor+=span
  x=legend_left+sum(col_widths[:i%3])+(i%3)*72;y=108+(i//3)*35
  p.append(f'<circle cx="{x+5}" cy="{y-7}" r="4" fill="{c}"/>');p.append(txt(language+' '+str(round(value/total*100,1))+'%',x+19,y,20))
 save('profile-cards',1120,136+((len(languages)-1)//3)*35,p)
 def shorten(t,n):return t if len(t)<=n else t[:n-3].rstrip()+'...'
 for repo in projects:
  title=repo['name'];desc=shorten(repo['description'] or 'Public repository',48)
  names=[key for key,_ in sorted(repo.get('languages',{}).items(),key=lambda x:-x[1])]
  language_text=' / '.join(names) or repo.get('language') or 'Public repository'
  while measure(language_text,17)>490:language_text=language_text[:-4].rstrip(' .')+'...'
  p=[f'<rect x="1" y="1" width="538" height="166" rx="13" stroke="{line}" fill="{panel}"/>',txt(shorten(title,31),22,43,24,ink,650),txt(desc,22,76,20,muted),txt(language_text,22,110,17,muted),txt('View repository',22,146,18,blue),logo('View repository',496,128,blue,size=22)]
  p[0]=f'<rect x="8" y="8" width="524" height="152" rx="13" stroke="{line}" fill="{panel}"/>'
  p.append(halo(8,8,524,152,blue,radius=13,weight=2))
  save('repo-'+title,540,168,p)
 from math import ceil
 footer_w=2*ceil((36+measure('Still version of landing page',22)+14)/2)
 save('still-link',footer_w,40,[f'<rect x="1" y="1" width="{footer_w-2}" height="38" rx="10" fill="{panel}" stroke="{line}"/>',logo('Pause',12,12,blue,size=18),txt('Still version of landing page',36,29,22,ink)])
 footer_w=2*ceil((38+measure('Back to top',20)+12)/2)
 save('back-top',footer_w,40,[f'<rect x="1" y="1" width="{footer_w-2}" height="38" rx="10" fill="{panel}" stroke="{line}"/>',logo('Back to top',12,11,blue,size=18),txt('Back to top',38,28,20,ink)])
