"""Crop rendered parts, add bounded contact shadows and export layout metadata."""
from pathlib import Path
import json
from PIL import Image,ImageFilter,ImageChops

A=Path(__file__).resolve().parents[1]/'assets/components3d'
meta=json.loads((A/'render-metadata.json').read_text(encoding='utf-8'))
a,c,b,d=meta['projection'];det=a*d-b*c;inverse=(d/det,-b/det,-c/det,a/det)
unit=meta['units_per_pixel'];origin=meta['resolution']/2
for level,part in meta['parts'].items():
 path=A/f'part-{level}.png';im=Image.open(path).convert('RGBA');alpha=im.getchannel('A')
 solid=alpha.point(lambda value:255 if value>64 else 0).getbbox()
 shadow=Image.new('RGBA',im.size,(0,12,5,0));shadow.putalpha(ImageChops.offset(alpha.filter(ImageFilter.GaussianBlur(4)),5,5).point(lambda value:round(value*.22)))
 im=Image.alpha_composite(shadow,im);crop=im.getchannel('A').point(lambda value:255 if value>4 else 0).getbbox()
 im.crop(crop).save(path,optimize=True)
 screen=[(solid[0]-origin)*unit,(solid[1]-origin)*unit,(solid[2]-origin)*unit,(solid[3]-origin)*unit]
 points=[((d*x-c*y)/det,(-b*x+a*y)/det) for x in [screen[0],screen[2]] for y in [screen[1],screen[3]]]
 part.update(polygon=points,screen_bounds=screen,bounds=[min(x for x,y in points),min(y for x,y in points),max(x for x,y in points),max(y for x,y in points)],image=[(crop[0]-origin)*unit,(crop[1]-origin)*unit,(crop[2]-crop[0])*unit,(crop[3]-crop[1])*unit])
meta['inverse']=inverse
(A/'layout.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
