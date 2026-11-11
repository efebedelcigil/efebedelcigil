import re,hashlib
from pathlib import Path


root = Path(__file__).resolve().parents[1]
content = (root/'README.md').read_text(encoding='utf-8')
content = content.replace('[Still version](docs/STATIC.md)', '[Animated version](../README.md)')
def still(match):
    path=match.group(0)
    candidate=root/path.replace('.svg','-still.svg')
    return path.replace('.svg','-still.svg') if candidate.is_file() else path
content=re.sub(r'assets/[^\"?#<>]+\.svg',still,content)
content = re.sub(r'(?<![/\w-])assets/', '../assets/', content)
content = content.replace('href="docs/STATIC.md','href="../README.md')
content = content.replace('<sub>[Still version](docs/STATIC.md)</sub>', '<sub>[Animated version](../README.md)</sub>')
def version(match):
    path=match.group(1);digest=hashlib.sha256((root/'docs'/path).read_bytes()).hexdigest()[:12]
    return path+'?v='+digest
content=re.sub(r'(\.\./assets/[^\"?#<>]+\.svg)(?:\?v=[a-f0-9]+)?',version,content)

(root/'docs/STATIC.md').write_text(content, encoding='utf-8')
