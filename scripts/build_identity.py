import argparse
import html
import math
import os
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

FONT = Path(os.environ.get('PROFILE_FONT', str(ROOT/'assets/fonts/SpaceGrotesk.ttf')))


@lru_cache(maxsize=12)
def font_at(weight=600, width=100):
    font = TTFont(FONT)
    if 'fvar' in font:
        axes = {axis.axisTag for axis in font['fvar'].axes}
        location = {key: value for key, value in {'wght': weight, 'wdth': width, 'opsz': 48}.items() if key in axes}
        return instantiateVariableFont(font, location, inplace=True)
    return font


def lettering(text, x, y, size, fill, weight=600, width=100, max_width=None):
    font = font_at(weight, width)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    pen = SVGPathPen(glyphs)
    cursor = 0
    for char in text:
        name = cmap.get(ord(char), '.notdef')
        glyphs[name].draw(TransformPen(pen, (1, 0, 0, 1, cursor, 0)))
        cursor += font['hmtx'][name][0]
    scale = size / font['head'].unitsPerEm
    if max_width is not None and cursor * scale > max_width:
        scale = max_width / cursor
    return f'<path aria-label="{html.escape(text, quote=True)}" d="{pen.getCommands()}" transform="translate({x} {y}) scale({scale:.6f} {-scale:.6f})" fill="{fill}"/>'


def build(theme, mobile=False):
    width,height=(360,205) if mobile else (640,296)
    ink='#edf2f8' if theme=='dark' else '#192a40'
    blue='#78a4ff' if theme=='dark' else '#214fc5'
    copper='#efa571' if theme=='dark' else '#b45e30'
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
           '<title id="title">Efe Varol Bedelcigil</title>',
           '<desc id="desc">Efe Varol Bedelcigil. Control systems and robotics.</desc>']
    if mobile:
        parts.append(lettering('Efe Varol',0,78,68,ink,650,100,352))
        parts.append(lettering('Bedelcigil',0,162,77,ink,800,100,352))
        parts.append(f'<path d="M4 185h244" stroke="{blue}" stroke-width="10"/>')
        parts.append(f'<circle cx="270" cy="185" r="5" fill="{copper}"/>')
    else:
        parts.append(lettering('Efe Varol',0,110,101,ink,650,100,628))
        parts.append(lettering('Bedelcigil',0,241,122,ink,800,100,628))
        parts.append(f'<path d="M5 275h433" stroke="{blue}" stroke-width="13"/>')
        parts.append(f'<circle cx="465" cy="275" r="6.5" fill="{copper}"/>')
    parts.append('</svg>')
    (ROOT/'assets'/('identity-'+('mobile-' if mobile else '')+theme+'.svg')).write_text('\n'.join(parts)+'\n',encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build vector profile identity from a locally installed font.')
    parser.add_argument('--font', type=Path, default=FONT)
    args = parser.parse_args()
    FONT = args.font
    if not FONT.is_file():
        parser.error('Font not found. Supply --font PATH or set PROFILE_FONT.')
    for theme in ('dark', 'light'):
        for mobile in (False, True):
            build(theme, mobile)
