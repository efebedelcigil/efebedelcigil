import re
from pathlib import Path


root = Path(__file__).resolve().parents[1]
content = (root/'README.md').read_text(encoding='utf-8')
content = content.replace('[Still version](docs/STATIC.md)', '[Animated version](../README.md)')
alt = re.search(r'<img src="assets/workbench.png"[^>]*alt="([^"]+)"',content)[1]
header = '<picture>\n'
header += '  <source media="(max-width: 600px)" srcset="assets/workbench-mobile.png">\n'
header += f'  <img src="assets/workbench.png" width="1440" alt="{alt}">\n</picture>'
content = re.sub(r'<picture>.*?</picture>',lambda match: header if 'assets/workbench' in match[0] else match[0],content,flags=re.S)
content = content.replace('assets/', '../assets/')
(root/'docs/STATIC.md').write_text(content, encoding='utf-8')
