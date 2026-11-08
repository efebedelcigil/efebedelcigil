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

FONT = Path(os.environ.get('PROFILE_FONT', str(Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts/bahnschrift.ttf')))


@lru_cache(maxsize=12)
def font_at(weight=600, width=100):
    font = TTFont(FONT)
    if 'fvar' in font:
        axes = {axis.axisTag for axis in font['fvar'].axes}
        location = {key: value for key, value in {'wght': weight, 'wdth': width}.items() if key in axes}
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
    width, height = (720, 280) if mobile else (1120, 258)
    dark = theme == 'dark'
    ink, secondary = ('#eef6ff', '#adc6df') if dark else ('#132e52', '#3c5877')
    cyan, blue, amber = ('#44e3e6', '#4b8dff', '#ffbe52') if dark else ('#008caa', '#075de8', '#ba6900')
    hairline = '#32557b' if dark else '#c3d4e6'
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
             '<title id="title">Efe Varol Bedelcigil</title>',
             '<desc id="description">Electrical and Electronics Engineering. Control systems and robotics. Personal identity with a gyroscope and a closed feedback loop.</desc>',
             f'<defs><linearGradient id="name" x1="0" x2="1"><stop stop-color="{cyan}"/><stop offset="1" stop-color="{blue}"/></linearGradient><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M1 1 9 5 1 9" fill="none" stroke="{cyan}" stroke-width="1.6"/></marker></defs>']
    if mobile:
        parts.append(f'<path d="M32 16h72m-72 7h44" stroke="{amber}" stroke-width="3"/>')
        parts.append(lettering('Efe Varol', 32, 99, 87, ink, 700, 90, 632))
        parts.append(lettering('Bedelcigil', 32, 194, 96, 'url(#name)', 700, 90, 650))
        parts.append(lettering('Control systems / Robotics', 36, 230, 27, secondary, 500, 100, 650))
        parts.append(f'<path d="M34 251h74l16-11 24 22 24-22 24 22 24-11h280" fill="none" stroke="{cyan}" stroke-width="2" marker-end="url(#arrow)"/>')
        parts.append(f'<circle cx="542" cy="251" r="5" fill="{amber}"/><circle cx="34" cy="251" r="4" fill="none" stroke="{cyan}" stroke-width="2"/>')
        parts.append(f'<g transform="translate(623 235)" fill="none" stroke="{blue}" stroke-width="2"><ellipse rx="35" ry="16" transform="rotate(-36)"/><ellipse rx="35" ry="16" transform="rotate(36)"/><circle r="14" stroke="{amber}"/></g>')
    else:
        parts.append(f'<path d="M40 18h64m-64 7h40" stroke="{amber}" stroke-width="3"/>')
        parts.append(lettering('Electrical & Electronics Engineering', 132, 27, 17, secondary, 500, 95))
        parts.append(lettering('Efe Varol', 36, 107, 92, ink, 700, 90, 680))
        parts.append(lettering('Bedelcigil', 36, 202, 104, 'url(#name)', 700, 90, 700))
        parts.append(lettering('Control systems / Robotics', 42, 247, 23, ink, 500, 100, 700))
        parts.append(f'<g transform="translate(900 121) scale(.72)" fill="none"><circle r="116" stroke="{hairline}" stroke-width="1"/><circle r="101" stroke="{blue}" stroke-width="2" stroke-dasharray="4 14"/><ellipse rx="104" ry="41" transform="rotate(-38)" stroke="{cyan}" stroke-width="3"/><ellipse rx="104" ry="41" transform="rotate(38)" stroke="{blue}" stroke-width="3"/><circle r="42" stroke="{amber}" stroke-width="6"/><path d="M-57 0H57M0-57V57" stroke="{hairline}" stroke-width="2"/><circle r="13" fill="{ink}" stroke="{cyan}" stroke-width="4"/></g>')
        parts.append(f'<path d="M770 121h52M978 121h94v109H770" fill="none" stroke="{cyan}" stroke-width="2" marker-end="url(#arrow)"/>')
        parts.append(f'<path d="M770 230v-14H42" fill="none" stroke="{hairline}" stroke-width="2"/>')
        parts.append(f'<circle cx="770" cy="121" r="7" fill="none" stroke="{amber}" stroke-width="2"/><circle cx="1072" cy="121" r="5" fill="{amber}"/>')
        parts.append(lettering('r(t)', 751, 102, 16, secondary, 500))
        parts.append(lettering('y(t)', 1048, 102, 16, secondary, 500))
        parts.append(lettering('Feedback & motion', 803, 251, 19, secondary, 500))
        for angle in range(0, 360, 30):
            a = math.radians(angle)
            x1, y1 = 900+88*math.cos(a), 121+88*math.sin(a)
            x2, y2 = 900+94*math.cos(a), 121+94*math.sin(a)
            parts.append(f'<path d="M{x1:.2f} {y1:.2f} {x2:.2f} {y2:.2f}" stroke="{amber if angle % 90 == 0 else hairline}" stroke-width="2"/>')
    parts.append('</svg>')
    name = 'identity-' + ('mobile-' if mobile else '') + theme + '.svg'
    (ROOT / 'assets' / name).write_text('\n'.join(parts) + '\n', encoding='utf-8')


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
