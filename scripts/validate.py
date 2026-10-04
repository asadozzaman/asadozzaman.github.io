"""Check generated routes, assets, metadata and fragment links before deployment."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.links=[]; self.h1=0; self.title=False; self.description=False; self.errors=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: self.errors.append('Duplicate ID: '+a['id'])
            self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='title': self.title=True
        if tag=='meta' and a.get('name')=='description': self.description=bool(a.get('content'))
        if tag=='img' and not a.get('alt'): self.errors.append('Missing image alt text')
        for attr in ('src','href'):
            if attr in a: self.links.append(a[attr])

pages={}
for file in OUT.rglob('*.html'):
    parser=Page(); parser.feed(file.read_text()); pages[file.resolve()]=parser
errors=[]
for file,page in pages.items():
    errors += [str(file.relative_to(OUT))+': '+x for x in page.errors]
    if page.h1!=1 or not page.title or not page.description: errors.append(str(file)+': heading or metadata missing')
    for raw in page.links:
        url=urlsplit(raw)
        if url.scheme or url.netloc: continue
        target=(OUT/unquote(url.path.lstrip('/'))) if url.path.startswith('/') else (file.parent/unquote(url.path))
        if not url.path: target=file
        if target.is_dir(): target=target/'index.html'
        target=target.resolve()
        if not target.is_relative_to(OUT): errors.append('Path escapes output: '+raw)
        elif not target.is_file(): errors.append(str(file.relative_to(OUT))+': missing '+raw)
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(str(file.relative_to(OUT))+': missing fragment '+raw)
for filename in ('source','evidence'):
    for frame in ('005','010','020'):
        if not (OUT/'assets'/f'{filename}_frame_{frame}.jpg').is_file(): errors.append('Missing explorer image')
data=json.loads((ROOT/'content/site.json').read_text())
for project in data['projects']:
    if not project['repository'].startswith('https://github.com/asadozzaman/'): errors.append('Unexpected project owner')
assert not errors, '\n'.join(errors)
print(f'PASS: {len(pages)} pages; local routes, fragments, images, metadata and evidence assets')
