import argparse
import html
import json
from pathlib import Path

import build_identity
from build_identity import lettering

ROOT = Path(__file__).resolve().parents[1]


def mobile_lines(group):
    if group['name'] == 'Code':
        return ['C · C++', 'Assembly']
    if group['name'] == 'Simulation':
        return ['MATLAB /', 'Simulink · PSIM']
    if group['name'] == 'Digital':
        return ['Quartus', 'ModelSim']
    return group['lines']


def build(theme, mobile, groups):
    width, height = (600, 410) if mobile else (1120, 270)
    dark = theme == 'dark'
    primary = '#eaf0fa' if dark else '#172a43'
    accents = {'teal': '#46d4ca', 'blue': '#8aa7ff', 'warm': '#e6a27d'} if dark else {'teal': '#007d78', 'blue': '#365dc1', 'warm': '#9c5635'}
    description = '. '.join(group['name'] + ': ' + ', '.join(group['lines']) for group in groups) + '.'
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
             '<title id="title">Engineering toolkit</title>',
             '<desc id="description">' + html.escape(description) + '</desc>']
    for index, group in enumerate(groups):
        row, column = divmod(index, 2)
        x=8+(300 if mobile else 560)*column
        y=12+(132 if mobile else 86)*row
        color=accents[group['color']]
        parts.append(lettering(group['name'],x,y+21,20,color,550))
        cursor=x
        lines=mobile_lines(group) if mobile else group['lines']
        for j,label in enumerate(lines):
            if mobile:
                bx,by=x,y+35+j*36
            else:
                bx,by=cursor,y+34
            bw=min(535,len(label)*12+24)
            fill='#17283e' if dark else '#edf3fa'
            parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="30" rx="7" fill="{fill}"/>')
            parts.append(lettering(label,bx+11,by+22,20,primary,550,100,bw-22))
            cursor+=bw+8
    parts.append('</svg>')
    name = 'toolkit-' + ('mobile-' if mobile else '') + theme + '.svg'
    (ROOT / 'assets' / name).write_text('\n'.join(parts) + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build the engineering toolkit typography from toolkit.json.')
    parser.add_argument('--font', type=Path, default=build_identity.FONT)
    args = parser.parse_args()
    build_identity.FONT = args.font
    if not args.font.is_file():
        parser.error('Font not found. Supply --font PATH or set PROFILE_FONT.')
    groups = json.loads((ROOT / 'assets/toolkit.json').read_text(encoding='utf-8'))
    if len(groups) > 6:
        raise ValueError('The toolkit supports up to six short groups.')
    for theme in ('light', 'dark'):
        for mobile in (False, True):
            build(theme, mobile, groups)
