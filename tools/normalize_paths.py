import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

replacements = [
    ("", ""),
    ("", ""),
    ("e:\\Bao Cao Ha Dung\\Tuan4-test\\Project\\", ""),
    ("e:\\Bao Cao Ha Dung\\Tuan4-test\\Project", ""),
    ("e:\\Bao Cao Ha Dung\\Tuan5-test\\Project\\", ""),
    ("e:\\Bao Cao Ha Dung\\Tuan5-test\\Project", ""),
    # also handle lowercase drive letter and single-backslash variants
    ("E:\\Bao Cao Ha Dung\\Tuan4-test\\Project\\", ""),
    ("E:\\Bao Cao Ha Dung\\Tuan5-test\\Project\\", ""),
]

skip_dirs = {'.git', '__pycache__', 'venv'}
text_exts = None  # None means try all files as text

modified = []
for path in ROOT.rglob('*'):
    if path.is_dir():
        if path.name in skip_dirs:
            continue
        else:
            continue
    if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.pdf', '.npz', '.zip', '.exe', '.dll'}:
        continue
    try:
        s = path.read_text(encoding='utf-8')
    except Exception:
        try:
            s = path.read_text(encoding='latin-1')
        except Exception:
            continue
    orig = s
    for old, new in replacements:
        s = s.replace(old, new)
    if s != orig:
        path.write_text(s, encoding='utf-8')
        modified.append(str(path.relative_to(ROOT)))

print(f"Modified {len(modified)} files:")
for p in modified:
    print(" - ", p)
