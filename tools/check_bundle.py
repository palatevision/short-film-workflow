"""Verify this review snapshot without network or external packages."""
from pathlib import Path
import hashlib, json, sys

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
expected = manifest['files_sha256']
entries = [
    entry
    for child in root.iterdir()
    if child.name != '.git'
    for entry in ([child, *child.rglob('*')] if child.is_dir() and not child.is_symlink() else [child])
]
files = {str(p.relative_to(root)): p for p in entries if p.is_file() and p != root / 'MANIFEST.json'}
errors = []
for p in entries:
    if p.is_symlink(): errors.append('Symbolic link: ' + str(p.relative_to(root)))
if set(files) != set(expected): errors.append('File list differs from manifest')
for rel, digest in expected.items():
    p = files.get(rel)
    if p is None or hashlib.sha256(p.read_bytes()).hexdigest() != digest:
        errors.append('Missing or changed file: ' + rel)
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('PASS: ' + str(len(expected)) + ' files verified; no media was generated.')
