import json
from pathlib import Path
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops, ImageStat


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT/'assets'


def geometry(path):
    tree = ET.parse(path)
    for node in tree.iter():
        for key in ('fill', 'stroke', 'stop-color', 'color'):
            node.attrib.pop(key, None)
    return ET.tostring(tree.getroot())


def main():
    report = {'vector_geometry': [], 'scenes': [], 'scene_theme_source': 'One canonical source per composition'}
    import re
    for block in re.findall(r'<picture>.*?</picture>',(ROOT/'README.md').read_text(encoding='utf-8'),re.S):
        if 'assets/workbench' in block:
            assert 'prefers-color-scheme' not in block
    for family in ('identity', 'toolkit'):
        for prefix in ('', 'mobile-'):
            stem = family+'-'+prefix
            assert geometry(ASSETS/(stem+'dark.svg')) == geometry(ASSETS/(stem+'light.svg')), stem
            report['vector_geometry'].append(stem+'theme geometry identical')
    for prefix in ('', '-mobile'):
        stem = 'workbench'+prefix
        with Image.open(ASSETS/(stem+'.png')) as png, Image.open(ASSETS/(stem+'-still.webp')) as still:
            difference = ImageChops.difference(png.convert('RGBA'), still.convert('RGBA'))
            assert all(high == 0 for low, high in difference.getextrema()), stem+'poster mismatch'
        with Image.open(ASSETS/(stem+'.webp')) as image:
            first = image.convert('RGBA')
            elapsed = 0
            for index in range(image.n_frames):
                image.seek(index)
                image.load()
                rgba = image.convert('RGBA')
                alpha = rgba.getchannel('A')
                box = alpha.getbbox()
                assert box and 0 < box[0] < box[2] < image.width and 0 < box[1] < box[3] < image.height, (stem,index,'cropped')
                assert alpha.getextrema() == (0,255), (stem,index,'alpha')
                elapsed += image.info.get('duration',0)
            assert elapsed == 12000, (stem,elapsed)
            loop = []
            for background in ('#0d1117','#ffffff'):
                base = Image.new('RGBA',image.size,background)
                a = Image.alpha_composite(base,first).convert('RGB')
                b = Image.alpha_composite(base,rgba).convert('RGB')
                loop.append(sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3)
            assert max(loop) < 1.5, (stem,'loop discontinuity',loop)
            report['scenes'].append({'variant':prefix or 'desktop','dimensions':image.size,
                'encoded_frames':image.n_frames,'duration_ms':elapsed,
                'loop_mean_delta_on_dark_and_light':loop,'all_frames_checked':True,
                'theme_files_identical':True,'poster_lossless_match':True,
                'bytes':(ASSETS/(stem+'.webp')).stat().st_size})
    target = ROOT/'.render/asset-checks.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
