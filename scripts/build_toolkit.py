import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICONS = {
    'code': '<path d="M11 6 2 16l9 10M27 6l9 10-9 10M22 3l-6 26"/>',
    'wave': '<path d="M2 29h34M4 30V2M4 19c4 0 4-13 8-13s4 20 8 20 4-16 8-16 4 9 8 9"/>',
    'chip': '<rect x="7" y="4" width="24" height="24" rx="3"/><rect x="13" y="10" width="12" height="12" rx="1"/><path d="M13 0v4M19 0v4M25 0v4M13 28v4M19 28v4M25 28v4M3 10h4M3 16h4M3 22h4M31 10h4M31 16h4M31 22h4"/>',
    'circuit': '<path d="M4 5h12v10h18M4 27h12V17M26 5v6M26 23v4"/><circle cx="3" cy="5" r="3"/><circle cx="3" cy="27" r="3"/><circle cx="26" cy="3" r="3"/><circle cx="26" cy="29" r="3"/><circle cx="35" cy="15" r="3"/>',
    'logic': '<path d="M3 8h7M3 24h7M10 2v28h8a14 14 0 0 0 0-28ZM32 16h6"/>',
    'terminal': '<rect x="1" y="3" width="36" height="27" rx="3"/><path d="m8 11 6 5-6 5M20 22h9"/>',
}


def build(theme, mobile, groups):
    width, height = (600,488) if mobile else (1120,272)
    colors = {'teal':'#67cabb','blue':'#84bfd9','warm':'#e9a28b'} if theme=='dark' else {'teal':'#167b6d','blue':'#367b99','warm':'#a2543c'}
    foreground, secondary = ('#e6edf3','#a9bacb') if theme=='dark' else ('#172d3d','#415d6c')
    heading, tools = (24,22) if mobile else (22,20)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
           '<title id="title">Engineering toolkit</title>',
           '<desc id="desc">'+html.escape('. '.join(group['name']+': '+', '.join(group['lines']) for group in groups))+'</desc>',
           f'<style>text{{font-family:"Segoe UI",Arial,sans-serif}}.heading{{font-size:{heading}px;font-weight:600;fill:{foreground}}}.tools{{font-size:{tools}px;fill:{secondary}}}.icon{{fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}</style>']
    for index,group in enumerate(groups):
        x,y=(12+300*(index%2),20+160*(index//2)) if mobile else (12+376*(index%3),28+136*(index//3))
        parts.append(f'<g transform="translate({x} {y})"><g class="icon" stroke="{colors[group["color"]]}">{ICONS[group["icon"]]}</g>')
        parts.append(f'<text class="heading" x="56" y="20">{html.escape(group["name"])}</text>')
        for row,line in enumerate(group['lines']):
            parts.append(f'<text class="tools" x="56" y="{56+32*row}">{html.escape(line)}</text>')
        parts.append('</g>')
    parts.append('</svg>')
    name='toolkit-'+('mobile-' if mobile else '')+theme+'.svg'
    (ROOT/'assets'/name).write_text('\n'.join(parts)+'\n',encoding='utf-8')


if __name__=='__main__':
    groups=json.loads((ROOT/'assets/toolkit.json').read_text(encoding='utf-8'))
    if len(groups)>6:
        raise ValueError('Keep the toolkit to six short groups.')
    for theme in ('light','dark'):
        for mobile in (False,True):
            build(theme,mobile,groups)
    readme=ROOT/'README.md'
    description='. '.join(group['name']+': '+', '.join(group['lines']) for group in groups)+'.'
    content=readme.read_text(encoding='utf-8')
    content=re.sub(r'(<img src="assets/toolkit-light.svg"[^>]*alt=")[^"]*(")',
                   lambda match: match[1]+html.escape(description,quote=True)+match[2],content)
    readme.write_text(content,encoding='utf-8')
