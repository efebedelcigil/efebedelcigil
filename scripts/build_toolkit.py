import argparse
import html
import json
from pathlib import Path

from vector_logos import logo
from vector_logos import logo
import build_identity
from build_identity import lettering

ROOT = Path(__file__).resolve().parents[1]


def mobile_lines(group):
    if group['name'] == 'Code':
        return ['C Ã‚Â· C++', 'Assembly']
    if group['name'] == 'Simulation':
        return ['MATLAB /', 'Simulink Ã‚Â· PSIM']
    if group['name'] == 'Digital':
        return ['Quartus', 'ModelSim']
    return group['lines']


def build(theme, mobile, groups):
    width,height=(600,470) if mobile else (1120,320)
    dark=theme=='dark'
    primary='#edf2f8' if dark else '#192a40'
    muted='#a9b8cc' if dark else '#52647a'
    accents={'teal':'#65c7c2','blue':'#8aa7ff','warm':'#efa571'} if dark else {'teal':'#147c79','blue':'#365dc1','warm':'#a75a2c'}
    description='. '.join(g['name']+': '+', '.join(g['tools']) for g in groups)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>Engineering toolkit</title><desc>{html.escape(description)}</desc>']
    icons={'code':'M2 4L-3 9l5 5m8-10 5 5-5 5M8 2 5 16','wave':'M-3 10c5-16 8 16 13 0s8 0 8 0','chip':'M0 3h14v14H0zM4 0v3m6-3v3M4 17v3m6-3v3M-3 7h3m-3 6h3m14-6h3m-3 6h3','circuit':'M-3 5h8l6 10h8M-3 15h8l6-10h8','logic':'M0 3v14h5c12 0 12-14 0-14zM-4 6h4m-4 8h4m13-4h7','terminal':'M-2 3l6 6-6 6m9 0h9'}
    columns=2 if mobile else 3
    cell=300 if mobile else 374
    panel_width=282 if mobile else 354
    for index,g in enumerate(groups):
        row,col=divmod(index,columns)
        x,y=8+col*cell,12+row*154
        color=accents[g['color']]
        line='#2c4059' if dark else '#d0ddeb'
        parts.append(f'<path d="M{x} {y+30}v96h{panel_width}" fill="none" stroke="{line}"/>')
        parts.append(f'<g transform="translate({x+5} {y+1})" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="{icons[g["icon"]]}"/></g>')
        parts.append(lettering(g['name'],x+34,y+18,21,primary,600))
        bx,by=x+12,y+38
        for label in g['tools']:
            bw=len(label)*10.4+51
            if bx+bw>x+panel_width-4:bx=x+12;by+=44
            fill='#16263b' if dark else '#edf3fa'
            parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="34" rx="10" fill="{fill}" stroke="{line}"/>')
            parts.append(f'<path d="M{bx+1} {by+11}v12" stroke="{color}" stroke-width="2.5"/>')
            parts.append(logo(label,bx+10,by+8,muted,fill))
            parts.append(lettering(label,bx+35,by+23,19,primary,550,100,bw-44))
            bx+=bw+8
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
