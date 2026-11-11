from functools import lru_cache
from labels import display_label
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path

from PIL import Image
from build_identity import font_at, lettering


ROOT=Path(__file__).resolve().parents[1]
INTRO_FRAMES=54
WORK_FRAMES=384
GLANCE_FRAMES=120
SOURCE_FRAMES=559
SCHEDULE=('work','glance','work','work','glance','work','glance','work','work','work','glance')
KNOB_KEYS=((0,0),(10.75,0),(12.0,10),(13.0,10),(14.15,0),(16,0))


def scheduled_frames(sequence):
    clips={'work':sequence[54:438],'glance':sequence[438:558]}
    return [frame for clip in SCHEDULE for frame in clips[clip]]


def underline_keys():
    result=[(0,0)]
    elapsed=0
    for clip in SCHEDULE:
        if clip=='work':
            result.extend((elapsed+t,value) for t,value in KNOB_KEYS[1:])
            elapsed+=16
        else:
            elapsed+=5
            result.append((elapsed,0))
    return result


def advances(text,size,weight,maximum):
    text=display_label(text)
    font=font_at(weight,100)
    cmap=font.getBestCmap()
    widths=[font['hmtx'][cmap[ord(char)]][0] for char in text]
    scale=min(size/font['head'].unitsPerEm,maximum/sum(widths))
    result=[0]
    for width in widths:
        result.append(result[-1]+width*scale)
    result[-1]+=3
    return result


def timeline(values,begin,duration):
    return f'<animate attributeName="href" values="{";".join(values)}" begin="{begin}s" dur="{duration}s" calcMode="discrete" '+('repeatCount="indefinite"' if begin else 'fill="freeze"')+'/>'


@lru_cache(maxsize=512)
def mobile_frame(data):
    with Image.open(io.BytesIO(base64.b64decode(data))) as image:
        image=image.convert('RGBA').resize((360,432),Image.Resampling.LANCZOS)
        buffer=io.BytesIO()
        image.save(buffer,format='WEBP',quality=80,method=4)
    return base64.b64encode(buffer.getvalue()).decode()


def make_svg(theme,mobile,images,sequence,background,steady,glance_background,still=False):
    width,height=(720,440) if mobile else (1280,540)
    ink='#edf2f8' if theme=='dark' else '#25394d'
    accent='#78a4ff' if theme=='dark' else '#365d94'
    copper='#efa571' if theme=='dark' else '#925c3c'
    lines=[('Efe Varol',8,86,55,650,400),('Bedelcigil',8,166,67,800,400)] if mobile else [('Efe Varol',22,250,90,650,720),('Bedelcigil',22,381,112,800,720)]
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
           '<title id="title">Efe Varol Bedelcigil</title>',
           '<desc id="desc">Control systems and robotics. A robot presses its control button, the name types in periodically, and the robot continues its own calibration cycle.</desc>',
           '<defs>']
    parts.append(f'<clipPath id="heroBounds"><rect x="0" y="0" width="{width}" height="{height}"/></clipPath>')
    parts.append(f'<image id="steady" width="600" height="720" href="data:image/png;base64,{steady}"/>')
    if not still:
        parts.append(f'<image id="background" width="600" height="720" href="data:image/webp;base64,{background}"/>')
        parts.append(f'<image id="glance-background" width="600" height="720" href="data:image/webp;base64,{glance_background}"/>')
        for index in sorted(set(sequence[:558])):
            data,kind=images[index]
            if mobile:data=mobile_frame(data)
            parts.append(f'<g id="r{index}" data-layer="{kind}">')
            background_id='background' if kind=='foreground' else 'glance-background'
            parts.append(f'<use href="#{background_id}"/>')
            parts.append(f'<image width="600" height="720" href="data:image/webp;base64,{data}"/></g>')
    for n,(text,x,y,size,weight,maximum) in enumerate(lines):
        values=advances(text,size,weight,maximum)
        parts.append(f'<clipPath id="line{n}"><rect x="0" y="0" width="{width}" height="{height}">')
        if not still:
            start=.80 if n==0 else 1.25
            duration=.45 if n==0 else .55
            times=[0,start]+[start+duration*i/(len(values)-1) for i in range(1,len(values))]+[38]+[38]+[38]+[38]+[38]+[38]+[38]
            clips=[0,0]+[x+value for value in values[1:]]+[width]+[width]+[width]+[width]+[width]+[width]+[width]
            keytimes=';'.join(f'{t/38:.6f}' for t in times)
            parts.append(f'<animate attributeName="width" values="{";".join(f"{v:.3f}" for v in clips)}" keyTimes="{keytimes}" begin="0s" dur="38s" calcMode="discrete" repeatCount="indefinite"/>')
        parts.append('</rect></clipPath>')
    parts.append('</defs>')
    for n,(text,x,y,size,weight,maximum) in enumerate(lines):
        parts.append(f'<g clip-path="url(#line{n})">'+lettering(text,x,y,size,ink,weight,100,maximum)+'</g>')
        if not still:
            values=advances(text,size,weight,maximum)
            begin=.8 if n==0 else 1.25
            duration=.45 if n==0 else .55
            parts.append(f'<rect x="{x}" y="{y-size*.78}" width="{max(4,size*.065)}" height="{size*.85}" fill="{accent}" opacity="0">')
            parts.append(f'<set attributeName="opacity" to="1" begin="{begin}s" dur="{duration}s"/>')
            parts.append(f'<animate attributeName="x" values="{";".join(f"{x+v:.3f}" for v in values)}" begin="{begin}s" dur="{duration}s" calcMode="discrete" fill="freeze"/>')
            parts.append('</rect>')
    baseline=244 if mobile else 425
    end=268 if mobile else 460
    start_x=lines[0][1]
    def response_line(amplitude):
        span=end-start_x
        return f'M{start_x} {baseline}C{start_x+span*.35} {baseline-amplitude} {start_x+span*.65} {baseline+amplitude*.65} {end} {baseline}'
    parts.append(f'<path id="underline" d="{response_line(0)}" fill="none" stroke="{accent}" stroke-width="1" opacity=".12">')
    if not still:
        keys=underline_keys()
        shapes=';'.join(response_line(value*(.6 if mobile else 1)) for _,value in keys)
        times=';'.join(f'{time/132:.9f}' for time,_ in keys)
        splines=';'.join(['.42 0 .58 1']*(len(keys)-1))
        parts.append(f'<animate attributeName="d" values="{shapes}" keyTimes="{times}" begin="2.25s" dur="132s" repeatCount="indefinite" calcMode="spline" keySplines="{splines}"/>')
    parts.append('</path>')
    span=end-start_x
    parts.append(f'<rect x="{start_x-5}" y="{baseline-7}" width="{span+10}" height="14" rx="7" stroke="{accent}" stroke-width=".8" fill="none" opacity=".5"/><path d="M{end+7} {baseline-2}v4" stroke="{accent}" stroke-width="2" stroke-linecap="round" opacity=".65"/>')
    parts.append(f'<clipPath id="chargeClip"><rect x="{start_x}" y="{baseline-5}" width="{span}" height="10" rx="3">')
    if not still:parts.append(f'<animate attributeName="width" values="0;{span};{span};0" keyTimes="0;.42;.78;1" dur="8s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .2 1;.4 0 .6 1;.4 0 .6 1"/>')
    parts.append('</rect></clipPath><g clip-path="url(#chargeClip)">')
    for weight,opacity in [(7,.08),(3,.25),(1.5,.85)]:
        parts.append(f'<path d="M{start_x} {baseline}h{span}" stroke="{accent}" stroke-width="{weight}" stroke-linecap="round" opacity="{opacity}"/>')
    if not still:
        parts.append(f'<path d="M{start_x} {baseline}h{span}" pathLength="100" stroke="{ink}" stroke-width="1.3" stroke-dasharray="4 96" opacity=".7"><animate attributeName="stroke-dashoffset" from="0" to="-100" dur="2s" repeatCount="indefinite"/></path>')
        parts.append(f'<g fill="none" stroke="{accent}" stroke-width=".8" opacity=".6"><path d="M-3 0l2 -1 1 2 2 -1m-1 -2l1 -1 1 1"><animate attributeName="opacity" values=".2;.7;.35;.6;.2" dur="1.3s" repeatCount="indefinite"/></path><animateMotion path="M{start_x} {baseline}h{span}" dur="2s" repeatCount="indefinite"/></g>')
    parts.append('</g>')
    identity=json.loads((ROOT/'assets/profile.json').read_text(encoding='utf-8'))
    muted='#a9b8cc' if theme=='dark' else '#53677d'
    ix,iy=(8,365) if mobile else (22,477)
    parts.append(lettering(identity['discipline'],ix,iy,20 if mobile else 25,muted,550,100,370 if mobile else 610))
    parts.append(lettering(identity['institution']+' / '+identity['status'],ix,iy+30,18 if mobile else 21,muted,450,100,370 if mobile else 610))
    rx,ry,rw=(275,-130,470) if mobile else (595,-215,720)
    parts.append(f'<g clip-path="url(#heroBounds)"><g transform="translate({rx} {ry}) scale({rw/600})"><use id="robotTrack" href="#steady">')
    if not still:
        parts.append(timeline([f'#r{i}' for i in sequence[:54]],0,2.25))
        parts.append(timeline([f'#r{i}' for i in scheduled_frames(sequence)],2.25,132))
    parts.append('</use></g></g></svg>')
    return '\n'.join(parts)+'\n'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--frames',type=Path,default=ROOT/'.render/portrait')
    args=parser.parse_args()
    files=sorted(args.frames.glob('[0-9][0-9][0-9][0-9].png'))
    expected=[args.frames/f'{frame:04d}.png' for frame in range(1,SOURCE_FRAMES+1)]
    if files!=expected:
        raise ValueError('Expected source frames 0001.png through 0559.png with no gaps.')
    steady_path=ROOT/'.render/portrait-steady.png'
    background_path=ROOT/'.render/portrait-background.png'
    glance_background_path=ROOT/'.render/portrait-glance-background.png'
    def resized(path):
        with Image.open(path) as image:
            if image.size!=(900,1080) or image.mode!='RGBA':
                raise ValueError(f'Expected a 900Ãƒâ€”1080 RGBA source: {path}')
            return image.resize((600,720),Image.Resampling.LANCZOS)
    buffer=io.BytesIO()
    resized(steady_path).save(buffer,format='PNG',optimize=True)
    steady=base64.b64encode(buffer.getvalue()).decode()
    def encoded_background(path):
        buffer=io.BytesIO()
        resized(path).save(buffer,format='WEBP',lossless=True,exact=True,method=4)
        return base64.b64encode(buffer.getvalue()).decode()
    background=encoded_background(background_path)
    glance_background=encoded_background(glance_background_path)
    for quality in (86,82,78,74):
        images={}
        hashes={}
        sequence=[]
        for source_index,file in enumerate(files):
            image=resized(file)
            kind='foreground' if source_index<438 else 'glance'
            digest=(kind,hashlib.sha256(image.tobytes()).hexdigest())
            if digest not in hashes:
                index=len(images)
                buffer=io.BytesIO()
                image.save(buffer,format='WEBP',quality=quality,method=4)
                images[index]=(base64.b64encode(buffer.getvalue()).decode(),kind)
                hashes[digest]=index
            sequence.append(hashes[digest])
        if max(len(make_svg(theme,mobile,images,sequence,background,steady,glance_background).encode())
               for theme in ('dark','light') for mobile in (False,True))<9_900_000:
            break
    else:
        raise ValueError('Hero exceeds the 9.9 MB asset budget.')
    for theme in ('dark','light'):
        for mobile in (False,True):
            for still in (False,True):
                name='hero-'+('mobile-' if mobile else '')+theme+('-still' if still else '')+'.svg'
                (ROOT/'assets'/name).write_text(make_svg(theme,mobile,images,sequence,background,steady,glance_background,still),encoding='utf-8')
    (ROOT/'.render/hero-build.json').write_text(json.dumps({'source_frames':559,'unique_frames':len(images),'frame_size':[600,720],
        'frame_quality':quality,'intro_seconds':2.25,'name_complete_seconds':1.8,'robot_loop_seconds':132,
        'work_seconds':16,'glance_seconds':5,'schedule':SCHEDULE,'scheduled_frames':len(scheduled_frames(sequence)),
        'backgrounds':['portrait-background.png','portrait-glance-background.png'],'background_encoding':'lossless WebP',
        'animated_bytes':(ROOT/'assets/hero-dark.svg').stat().st_size},indent=2)+'\n',encoding='utf-8')
    print((ROOT/'.render/hero-build.json').read_text())


if __name__=='__main__':
    main()
