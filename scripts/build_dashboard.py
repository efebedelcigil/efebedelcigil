from labels import display_label
from pathlib import Path
import json,html,re,xml.etree.ElementTree as E,datetime
from build_identity import lettering
from circuit_route import circuit_route,spark_gate
from contribution_geometry import BoardGeometry
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
 dates=sorted(public['days']);cells,weeks=cell_map(public['days']);geometry=BoardGeometry(weeks);chip=geometry.chip;cw,ch=chip.width,chip.height;step=geometry.step;pitch=geometry.row_pitch;palette=['#172536']+['#293a4b']*4 if theme=='dark' else ['#c1cedb']+['#42576b']*4
 panel,line=('#142c36','#375262') if theme=='dark' else ('#d6e3e5','#9fb5bd')
 if theme=='light':muted='#53677d'
 die_colors=['','#79b8dc','#d98940','#ffc04a','#fff1bc'] if theme=='dark' else ['','#6eb3d7','#ca7a39','#f0b333','#fff2cb']
 period=datetime.date.fromisoformat(dates[0]).strftime('%b %Y')+' / '+datetime.date.fromisoformat(dates[-1]).strftime('%b %Y')
 p=[centered(str(sum(public['day_counts'].values()))+' public contributions',1120,26,22,blue,600),centered(period,1120,51,17,muted)]
 p.append(f'<g transform="{geometry.transform}"><rect x="0" y="4" width="{geometry.width}" height="{geometry.height}" rx="18" fill="{line}"/><rect width="{geometry.width}" height="{geometry.height}" rx="18" fill="{panel}" stroke="{muted}" stroke-width=".7"/>')
 p.append(halo(0,0,geometry.width,geometry.height,copper,radius=18,weight=2.1,electric=False))
 # Silkscreen and copper stay in the clear perimeter, outside every day cell.
 for side in [0,1]:
  x=7 if not side else geometry.width-7
  p.append(f'<path d="M{x} 22v{geometry.height-44}" stroke="{copper}" stroke-width=".8" opacity=".45"/>')
  for y in [12,geometry.height-12]:p.append(f'<circle cx="{x}" cy="{y}" r="2.7" fill="{palette[0]}" stroke="{copper}" stroke-width="1.3"/>')
 for col in range(0,weeks,6):
  x=geometry.padding+(col+.5)*step
  p.append(f'<path d="M{x} 8h{step*2}l5 5h{step}" fill="none" stroke="{copper}" stroke-width=".8" opacity=".38"/><circle cx="{x}" cy="8" r="1.6" fill="{panel}" stroke="{copper}" stroke-width=".8"/>')
 for week in range(weeks+1):p.append(f'<path data-grid="vertical" d="M{geometry.padding+week*step} {geometry.padding}v{7*pitch}" stroke="{line}" stroke-width=".7" opacity=".4"/>')
 for row in range(8):p.append(f'<path data-grid="horizontal" d="M{geometry.padding} {geometry.padding+row*pitch}h{weeks*step}" stroke="{line}" stroke-width=".7" opacity=".4"/>')
 chip_start=len(p);empty_pads=[]
 for d in dates:
  week,row=cells[d];level=public['days'][d];x,y=geometry.origin((week,row))
  if not level:
   empty_pads.append(f'<rect data-date="{d}" data-level="0" x="{x}" y="{y}" width="{cw}" height="{ch}" rx=".7" fill="{palette[0]}" opacity=".35" stroke="{line}" stroke-width=".4"/><path d="M{x+1} {y+ch/2}h2m{cw-6} 0h2" stroke="{muted}" stroke-width="2" opacity=".25"/>');continue
  x,y=geometry.package_origin((week,row),level);lift=chip.lift(level)
  left,top,right,bottom=chip.bounds(x,y,level)
  p.append(f'<rect data-chip-matte="{d}" x="{left}" y="{top}" width="{right-left}" height="{bottom-top}" rx="2" fill="{panel}"/>')
  p.append(f'<rect x="{x+1}" y="{y+2}" width="{cw+1}" height="{ch+1}" rx="2" fill="{line}" opacity=".7"/>')
  for py in [2.5,5.5,8.5,11.5]:
   p.append(f'<path data-chip-pin="{d}" d="M{x-2} {y+py}h1v{-lift*.5}h2M{x+cw+3} {y+py}h-1v{-lift*.5}h-3" fill="none" stroke="{muted}" stroke-width="1.3" stroke-linejoin="round"/>')
  p.append(f'<path d="M{x} {y+ch-lift}h{cw}v{lift}h{-cw}z" fill="{line}"/><path d="M{x+cw} {y-lift}v{ch}l2 2V{y+2}z" fill="{muted}" opacity=".6"/>')
  p.append(f'<rect x="{x}" y="{y-lift}" width="{cw}" height="{ch}" rx=".6" data-date="{d}" data-level="{level}" fill="{palette[level]}" stroke="{muted}" stroke-width=".5"><title>{d}: {public["day_counts"][d]} public contributions, level {level}</title></rect>')
  p.append(f'<path d="M{x+1} {y+2-lift}h{cw-2}" stroke="{ink}" stroke-width=".7" opacity=".45"/>')
  die_w=cw-4;die_h=4;die_color=die_colors[level]
  p.append(f'<rect data-die="{d}" data-level="{level}" x="{x+2}" y="{y-lift+ch-5}" width="{die_w}" height="{die_h}" rx=".4" fill="{die_color}"/>')
  p.append(f'<circle cx="{x+2.5}" cy="{y-lift+2.5}" r=".8" fill="{muted}"/><path d="M{x+5} {y-lift+3}h4m-4 2h3" stroke="{muted}" stroke-width=".6" opacity=".75"/>')
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
 from math import hypot
 distances=[0.0]
 for a,b in zip(points,points[1:]):distances.append(distances[-1]+hypot(b[0]-a[0],b[1]-a[1]))
 total_length=distances[-1] or 1
 for cell in sorted(active):
  x,y=geometry.package_origin(cell,levels[cell]);lift=chip.lift(levels[cell])
  phase=max(0,distances[route.index(cell)]/total_length*14-.25)
  p.append(f'<rect x="{x+3}" y="{y+ch-lift/2-.5}" width="{cw-6}" height="1" rx=".5" fill="{copper}" opacity=".12"><animate attributeName="opacity" values=".12;.7;.12;.12" keyTimes="0;.025;.065;1" begin="{phase:.3f}s" dur="14s" repeatCount="indefinite"/></rect>')
 p.append('</g>')
 p.append(txt('Less',355,388,18,muted))
 for level in range(5):
  x=419+level*52;lift=chip.lift(level) if level else 0;top=371-lift
  p.append(f'<path d="M{x} {top+20}h28v{lift}h-28z" fill="{line}"/>')
  p.append(f'<rect x="{x}" y="{top}" width="28" height="20" rx="3" fill="{palette[level]}" stroke="{muted}" stroke-width=".5"/>')
  if level:
   for py in [3,7,11,15,19]:p.append(f'<path d="M{x-4} {top+py}h4m28 0h4" stroke="{muted}" stroke-width="1.5"/>')
   dc=die_colors[level]
   p.append(f'<rect x="{x+4}" y="{top+12}" width="20" height="5" rx=".5" fill="{dc}"/><circle cx="{x+5}" cy="{top+4}" r="1.2" fill="{muted}"/><path d="M{x+10} {top+4}h11m-11 3h8" stroke="{muted}" stroke-width="1"/>')
  p.append(txt(str(level),x+9,414,15,muted))
 p.append(txt('More',697,388,18,muted))
 save('contribution',1120,430,p)
 save('contribution-still',1120,430,[strip_motion(part) for part in p])
 if theme=='light':panel,line,muted='#e4ebf1','#bdcbd9','#53677d'
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
  p[0]=f'<rect x="5" y="5" width="530" height="158" rx="13" stroke="{line}" fill="{panel}"/>'
  p.append(halo(5,5,530,158,blue,radius=13,weight=2))
  save('repo-'+title,540,168,p)
 save('still-link',400,40,[f'<rect x="1" y="1" width="398" height="38" rx="10" fill="{panel}" stroke="{line}"/>',logo('Pause',12,12,blue,size=18),txt('Still version of landing page',36,29,22,ink)])

 save('back-top',190,40,[f'<rect x="1" y="1" width="188" height="36" rx="9" fill="{panel}" stroke="{line}"/>',logo('Back to top',12,9,blue,size=18),txt('Back to top',38,26,20,ink)])
