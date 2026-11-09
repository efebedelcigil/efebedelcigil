import re
from pathlib import Path


root = Path(__file__).resolve().parents[1]
content = (root/'README.md').read_text(encoding='utf-8')
content = content.replace('[Still version](docs/STATIC.md)', '[Animated version](../README.md)')
content = re.sub(r'assets/(hero-(?:mobile-)?(?:dark|light))\.svg',r'assets/\1-still.svg',content)
content = content.replace('assets/contribution-dark.svg','assets/contribution-still-dark.svg').replace('assets/contribution-light.svg','assets/contribution-still-light.svg')
content = content.replace('assets/', '../assets/')
content = content.replace('href="docs/STATIC.md"','href="../README.md"')
content = content.replace('<sub>[Still version](docs/STATIC.md)</sub>', '<sub>[Animated version](../README.md)</sub>')
(root/'docs/STATIC.md').write_text(content, encoding='utf-8')
