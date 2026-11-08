import re
from pathlib import Path


root = Path(__file__).resolve().parents[1]
content = (root/'README.md').read_text(encoding='utf-8')
content = content.replace('[Still version](docs/STATIC.md)', '[Animated version](../README.md)')
alt = re.search(r'<img src="assets/workbench-light.png"[^>]*alt="([^"]+)"',content)[1]
header = '<picture>\n'
for condition,name in [
    ('(max-width: 600px) and (prefers-color-scheme: dark)','mobile-dark'),
    ('(max-width: 600px)','mobile-light'),
    ('(prefers-color-scheme: dark)','dark')
]:
    header += f'  <source media="{condition}" srcset="assets/workbench-{name}.png">\n'
header += f'  <img src="assets/workbench-light.png" width="1120" alt="{alt}">\n</picture>'
content = re.sub(r'<picture>.*?</picture>',lambda match: header,content,count=1,flags=re.S)
content = content.replace('assets/', '../assets/')
(root/'docs/STATIC.md').write_text(content, encoding='utf-8')
