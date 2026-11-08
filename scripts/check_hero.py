import argparse
import base64
import io
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops
from build_hero import SCHEDULE, underline_keys

ROOT=Path(__file__).resolve().parents[1]
NS={'s':'http://www.w3.org/2000/svg'}


def structural(path):
    tree=ET.parse(path)
    for node in tree.iter():
        for key in ('fill','stroke','stop-color','color'):
            node.attrib.pop(key,None)
    return ET.tostring(tree.getroot())


def decode(href):
    assert href.startswith(('data:image/webp;base64,','data:image/png;base64,')),href[:40]
    with Image.open(io.BytesIO(base64.b64decode(href.split(',',1)[1],validate=True))) as image:
        image.load()
        assert image.size==(600,720),image.size
        assert image.mode=='RGBA',image.mode
        return image.copy()


def check_svg(path, mobile, still, expected_steady, decode_images=False, expected_backgrounds=None):
    expected_backgrounds=expected_backgrounds or {}
    tree=ET.parse(path)
    root=tree.getroot()
    width,height=(720,440) if mobile else (1280,540)
    assert root.get('viewBox')==f'0 0 {width} {height}'
    nodes={node.get('id'):node for node in tree.iter() if node.get('id')}
    assert len(nodes)==sum(bool(node.get('id')) for node in tree.iter()),'duplicate IDs'
    decoded=0
    for node in tree.iter():
        assert not node.tag.endswith(('script','foreignObject'))
        assert not any(key.lower().startswith('on') for key in node.attrib)
        references=[node.get('href','')]
        if node.get('attributeName')=='href':
            references+=node.get('values','').split(';')
        for href in references:
            if href.startswith('#'):
                assert href[1:] in nodes,href
            elif href:
                assert node.tag.endswith('image'),href[:40]
                if decode_images or node.get('id')=='steady' or node.get('id') in expected_backgrounds:
                    image=decode(href)
                    decoded+=1
                    if node.get('id')=='steady':
                        assert href.startswith('data:image/png;base64,')
                        assert all(high==0 for low,high in ImageChops.difference(image,expected_steady).getextrema()),'steady mismatch'
                    if node.get('id') in expected_backgrounds:
                        expected=expected_backgrounds[node.get('id')]
                        assert all(high==0 for low,high in ImageChops.difference(image,expected).getextrema()),'background mismatch'
        for value in node.attrib.values():
            for reference in re.findall(r'url\(#([^\)]+)\)',value):
                assert reference in nodes,reference
    assert path.stat().st_size<9_900_000,path
    crop=nodes['heroBounds'].find('s:rect',NS)
    assert crop.attrib=={'x':'0','y':'0','width':str(width),'height':str(height)}
    assert tree.find('.//s:g[@clip-path="url(#heroBounds)"]',NS) is not None
    robot=nodes['robotTrack']
    assert robot.get('href')=='#steady','No-motion default must be the full steady image'
    for name in ('line0','line1'):
        rectangle=nodes[name].find('s:rect',NS)
        assert float(rectangle.get('width'))==width,'Name must be readable without SMIL'
        if not still:
            animation=rectangle.find('s:animate',NS)
            assert animation is not None and animation.get('repeatCount')=='indefinite'
            assert animation.get('begin')=='0s'
            assert float(animation.get('dur')[:-1])==38
    if still:
        assert not tree.findall('.//s:animate',NS) and not tree.findall('.//s:set',NS)
        assert set(nodes)=={'title','desc','heroBounds','steady','line0','line1','underline','robotTrack'}
        return decoded
    groups={key:node for key,node in nodes.items() if key.startswith('r') and key!='robotTrack'}
    assert groups
    for key,node in groups.items():
        assert node.tag.endswith('g') and node.get('data-layer') in ('foreground','glance'),key
        background=node.find('s:use',NS)
        assert background is not None,key
        expected_background='#background' if node.get('data-layer')=='foreground' else '#glance-background'
        assert background.get('href')==expected_background,key
        assert list(node)[0] is background,'Background must precede the arm'
        assert len(node.findall('s:image',NS))==1,key
    assert 'background' in nodes and 'glance-background' in nodes
    tracks=robot.findall('s:animate',NS)
    assert len(tracks)==2
    assert tracks[0].get('begin')=='0s' and tracks[0].get('dur')=='2.25s' and tracks[0].get('fill')=='freeze'
    assert not tracks[0].get('repeatCount')
    assert tracks[1].get('begin')=='2.25s' and tracks[1].get('dur')=='132s' and tracks[1].get('repeatCount')=='indefinite'
    intro=tracks[0].get('values').split(';')
    repeating=tracks[1].get('values').split(';')
    assert len(intro)==54 and len(repeating)==3168
    assert all(groups[ref[1:]].get('data-layer')=='foreground' for ref in intro)
    offset=0
    seen={}
    for clip in SCHEDULE:
        count=384 if clip=='work' else 120
        values=repeating[offset:offset+count]
        expected='foreground' if clip=='work' else 'glance'
        assert all(groups[ref[1:]].get('data-layer')==expected for ref in values),(clip,offset)
        if clip in seen:
            assert values==seen[clip],f'{clip} raster IDs must be reused'
        seen[clip]=values
        offset+=count
    assert offset==3168
    underline=nodes['underline'].find('s:animate',NS)
    assert underline.get('begin')=='2.25s' and underline.get('dur')=='132s'
    assert underline.get('repeatCount')=='indefinite'
    times=[float(value) for value in underline.get('keyTimes').split(';')]
    assert len(times)==len(underline_keys())
    assert all(abs(time-expected/132)<1e-8 for time,(expected,_) in zip(times,underline_keys()))
    assert all(a<b for a,b in zip(times,times[1:]))
    assert len(underline.get('values').split(';'))==len(times)
    assert len(underline.get('keySplines').split(';'))==len(times)-1
    return decoded


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--frames',type=Path,default=ROOT/'.render/portrait')
    args=parser.parse_args()
    with Image.open(ROOT/'.render/portrait-steady.png') as source:
        assert source.size==(900,1080) and source.mode=='RGBA'
        expected_steady=source.resize((600,720),Image.Resampling.LANCZOS)
    expected_backgrounds={}
    for key,file in [('background','portrait-background.png'),('glance-background','portrait-glance-background.png')]:
        with Image.open(ROOT/'.render'/file) as source:
            assert source.size==(900,1080) and source.mode=='RGBA',file
            assert source.getchannel('A').getextrema()==(0,255),file
            expected_backgrounds[key]=source.resize((600,720),Image.Resampling.LANCZOS)
    report={'theme_pairs':[],'frames_decoded':0,'source_frames':0,'intro_seconds':2.25,
            'name_complete_seconds':1.8,'loop_seconds':132,'work_seconds':16,'glance_seconds':5,
            'schedule':SCHEDULE,'scheduled_frames':3168,'shared_backgrounds':['work','glance'],
            'glance_arm_only':True,'lossless_background_match':True}
    for size in ('','mobile-'):
        for mode in ('','-still'):
            a=ROOT/'assets'/f'hero-{size}dark{mode}.svg'
            b=ROOT/'assets'/f'hero-{size}light{mode}.svg'
            assert structural(a)==structural(b),(size,mode)
            for path in (a,b):
                report['frames_decoded']+=check_svg(path,bool(size),bool(mode),expected_steady,path.name=='hero-dark.svg',expected_backgrounds)
            report['theme_pairs'].append({'size':size or 'desktop','mode':mode or 'animated','same_geometry':True})
    files=sorted(args.frames.glob('[0-9][0-9][0-9][0-9].png'))
    assert files==[args.frames/f'{frame:04d}.png' for frame in range(1,560)],'Expected 559 consecutive source frames'
    for index,file in enumerate(files):
        with Image.open(file) as image:
            assert image.size==(900,1080) and image.mode=='RGBA',file
            alpha=image.getchannel('A')
            box=alpha.getbbox()
            assert box and alpha.getextrema()==(0,255),file
            # Close-ups may intentionally touch the portrait border. The explicit
            # heroBounds clip contains them in the final SVG viewport.
            if index<438:
                assert 0<box[0]<box[2]<image.width and 0<box[1]<box[3]<image.height,file
            report['source_frames']+=1
    static=(ROOT/'docs/STATIC.md').read_text(encoding='utf-8')
    assert all('-still.svg' in reference for reference in re.findall(r'(?:src|srcset)="([^"]*hero-[^"]*\.svg)"',static))
    for path in (ROOT/'README.md',ROOT/'docs/STATIC.md'):
        for reference in re.findall(r'(?:src|srcset)="([^"]+)"',path.read_text(encoding='utf-8')):
            if reference.startswith('https://komarev.com/ghpvc/?username=efebedelcigil'): continue
            assert (path.parent/reference).is_file(),(path,reference)
    (ROOT/'.render/hero-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
