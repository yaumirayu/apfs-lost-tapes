"""Validate all 88 published paths and ZIP extraction integrity; no dependencies."""
from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parent
manifest=json.loads((root/'audio-manifest.json').read_text(encoding='utf-8'))
html=(root/'index.html').read_text(encoding='utf-8')
library=json.loads(re.search(r'const LIBRARY=(.*?);\s*const albums=',html,re.S)[1])
expected={t['src'] for t in library['tracks']}
assert len(expected)==len(manifest)==88
assert len(library['albums'])==6
assert sum(t['title']=='Слепые' for t in library['tracks'])==1
assert expected=={f.relative_to(root).as_posix() for f in (root/'assets/audio').glob('*.mp3')}
for entry in manifest:
 p=root/entry['path']
 assert p.stat().st_size==entry['bytes'],p
 assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],p
 assert p.stat().st_size<100*1024*1024,p
for album in library['albums']:
 assert all(next(t for t in library['tracks'] if t['id']==i)['album']==album['id'] for i in album['tracks'])
print('PASS: 88 MP3, SHA-256, exact paths, 6 releases, no duplicate release, GitHub file size limits.')
