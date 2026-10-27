"""Минификация собственных CSS/JS без внешних пакетов."""
import re
from pathlib import Path
root = Path(__file__).resolve().parents[1] / 'public/assets'
for name in ['style.css', 'app.js']:
    source = (root / name).read_text()
    source = re.sub(r'/\*.*?\*/', '', source, flags=re.S)
    if name.endswith('.js'):
        source = re.sub(r'^\s*//.*$', '', source, flags=re.M)
    source = '\n'.join(line.strip() for line in source.splitlines() if line.strip())
    if name.endswith('.css'):
        source = re.sub(r'\s*([{};:,])\s*', r'\1', source)
    (root / name.replace('.', '.min.', 1)).write_text(source + '\n')
    print(name, len((root/name).read_bytes()), '->', len(source.encode()))
