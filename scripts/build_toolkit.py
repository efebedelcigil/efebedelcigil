import argparse
import html
import json
import re
from pathlib import Path

import build_identity
from build_identity import lettering

ROOT = Path(__file__).resolve().parents[1]
ICONS = {
    'code': '<path d="M17 13 5 28l12 15M39 13l12 15-12 15"/><path d="m33 8-10 40" stroke="ACCENT"/>',
    'wave': '<path d="M5 47h47M8 48V6" opacity=".45"/><path d="M8 30c7 0 7-19 14-19s7 32 14 32 7-26 14-26"/><circle cx="22" cy="11" r="3" fill="ACCENT" stroke="none"/><path d="M36 43h15" stroke="ACCENT"/>',
    'chip': '<rect x="12" y="12" width="32" height="32" rx="5" fill="COLOR" fill-opacity=".1"/><rect x="20" y="20" width="16" height="16" rx="2" stroke="ACCENT"/><path d="M18 5v7m10-7v7m10-7v7M18 44v7m10-7v7m10-7v7M5 18h7m-7 10h7m-7 10h7m32-20h7m-7 10h7m-7 10h7"/>',
    'circuit': '<path d="M6 11h17v17h26M6 45h17V31M38 7v12M38 37v12"/><circle cx="6" cy="11" r="4" fill="COLOR" fill-opacity=".2"/><circle cx="6" cy="45" r="4"/><circle cx="38" cy="7" r="4" stroke="ACCENT"/><circle cx="38" cy="49" r="4" stroke="ACCENT"/><circle cx="49" cy="28" r="4" fill="ACCENT" stroke="none"/><path d="M32 23h12v10H32z" stroke="ACCENT"/>',
    'logic': '<path d="M3 16h12M3 39h12M15 8v39h9a19.5 19.5 0 0 0 0-39ZM44 28h10"/><path d="M5 54h8v-5h8v5h8" stroke="ACCENT"/><circle cx="52" cy="28" r="3" fill="ACCENT" stroke="none"/>',
    'terminal': '<rect x="3" y="7" width="50" height="39" rx="5" fill="COLOR" fill-opacity=".08"/><path d="m13 19 10 8-10 8" stroke="ACCENT"/><path d="M31 36h12M18 52h20M28 46v6"/><circle cx="46" cy="13" r="2" fill="ACCENT" stroke="none"/>',
}


def build(theme, mobile, groups):
    width, height = (600, 668) if mobile else (1120, 366)
    dark = theme == 'dark'
    colors = {'teal': '#49d7ca', 'blue': '#68a5ff', 'warm': '#ffbe60'} if dark else {'teal': '#008a83', 'blue': '#075fe1', 'warm': '#aa6000'}
    foreground, secondary = ('#edf5ff', '#b9cde1') if dark else ('#153153', '#435f7c')
    accent = '#ffbe60' if dark else '#b86b05'
    hairline = '#294c70' if dark else '#c4d7ea'
    description = '. '.join(group['name'] + ': ' + ', '.join(group['lines']) for group in groups) + '.'
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
             '<title id="title">Engineering toolkit</title>',
             '<desc id="description">' + html.escape(description) + '</desc>']
    for index, group in enumerate(groups):
        x, y = (12 + 300*(index % 2), 12 + 218*(index // 2)) if mobile else (12 + 376*(index % 3), 18 + 180*(index // 3))
        color = colors[group['color']]
        icon = ICONS[group['icon']].replace('COLOR', color).replace('ACCENT', accent)
        parts.append(f'<g transform="translate({x} {y})">')
        parts.append(f'<path d="M-2 17a38 38 0 0 1 63 0M1 46a38 38 0 0 0 59 1" fill="none" stroke="{color}" stroke-width="1" opacity=".3"/>')
        parts.append(f'<g transform="translate(0 10)" fill="none" stroke="{color}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{icon}</g>')
        text_x = 74 if mobile else 84
        parts.append(lettering(group['name'], text_x, 38, 32 if mobile else 27, foreground, 700, 90, 214 if mobile else 255))
        lines = ['Quartus', 'ModelSim'] if mobile and group['icon'] == 'logic' else group['lines']
        for row, line in enumerate(lines):
            parts.append(lettering(line, text_x, (86 + 38*row) if mobile else (80 + 32*row), 28 if mobile else 22, secondary, 500, 90, 214 if mobile else 254))
        rule_y = 171 if mobile else 129
        parts.append(f'<path d="M8 {rule_y+8}h28l8-8h218" fill="none" stroke="{hairline}" stroke-width="1.5"/><path d="M44 {rule_y}h34" stroke="{color}" stroke-width="3"/><circle cx="266" cy="{rule_y}" r="3" fill="{color}"/>')
        parts.append('</g>')
    parts.append('</svg>')
    name = 'toolkit-' + ('mobile-' if mobile else '') + theme + '.svg'
    (ROOT / 'assets' / name).write_text('\n'.join(parts) + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build vector engineering toolkit from toolkit.json.')
    parser.add_argument('--font', type=Path, default=build_identity.FONT)
    args = parser.parse_args()
    build_identity.FONT = args.font
    if not args.font.is_file():
        parser.error('Font not found. Supply --font PATH or set PROFILE_FONT.')
    groups = json.loads((ROOT / 'assets/toolkit.json').read_text(encoding='utf-8'))
    if len(groups) > 6:
        raise ValueError('The toolkit supports up to six groups.')
    for theme in ('light', 'dark'):
        for mobile in (False, True):
            build(theme, mobile, groups)
    readme = ROOT / 'README.md'
    description = '. '.join(group['name'] + ': ' + ', '.join(group['lines']) for group in groups) + '.'
    content = readme.read_text(encoding='utf-8')
    content = re.sub(r'(<img src="assets/toolkit-light.svg"[^>]*alt=")[^"]*(")', lambda match: match[1] + html.escape(description, quote=True) + match[2], content)
    readme.write_text(content, encoding='utf-8')
