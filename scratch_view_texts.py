import json
from pathlib import Path

# Resolve workspace BASE path (works when running from root or common subfolders)
cwd = Path.cwd()
if cwd.name in ["data", "src", "notebookes", "results"]:
    BASE = cwd.parent
else:
    BASE = cwd

IN_FILE = BASE / "data" / "processed" / "hidden_v2.json"
OUT_FILE = BASE / "scratch_texts.txt"

if not IN_FILE.exists():
    print(f"[ERROR] Input file not found: {IN_FILE}")
else:
    with open(IN_FILE, encoding='utf-8') as f:
        p = json.load(f)
    with open(OUT_FILE, 'w', encoding='utf-8') as out:
        for x in p:
            out.write(f"{x['task_id']}: {x.get('text','')}\n")
    print(f"Done writing to {OUT_FILE}")
