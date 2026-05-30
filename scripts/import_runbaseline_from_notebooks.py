import os
from pathlib import Path
import importlib
import sys

os.chdir(Path('notebooks').resolve())
print('CWD (simulated notebook):', Path.cwd())
# Simulate notebook's sys.path insertion
proj_root = Path.cwd().parent
src_path = str(proj_root / 'src')
print('Inserting to sys.path:', src_path)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import run_baseline as module
import run_baseline
print('module run_baseline imported')
print('BASE ->', run_baseline.BASE)
print('DATASET_FILE ->', run_baseline.DATASET_FILE)
print('Exists ->', run_baseline.DATASET_FILE.exists())
