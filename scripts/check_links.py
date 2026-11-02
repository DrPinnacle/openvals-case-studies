"""Validate local Markdown path targets; external links are excluded."""
from pathlib import Path
import re
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
count=0
for source in ROOT.rglob('*.md'):
    if '.git' in source.parts: continue
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',source.read_text()):
        if re.match(r'^[a-zA-Z][\w+.-]*:',target):continue
        path=unquote(target).partition('#')[0]
        if path and not (source.parent/path).exists():raise SystemExit(f'Missing: {source}: {target}')
        count+=1
print(f'PASS: {count} local Markdown links; external URLs excluded')
