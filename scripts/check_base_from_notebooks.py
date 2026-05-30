import os
from pathlib import Path
import runpy

os.chdir(Path('notebooks').resolve())
print('CWD (simulated notebook):', Path.cwd())
ns = runpy.run_path('src/run_baseline.py')
print('BASE from run_baseline.py ->', ns.get('BASE'))
print('DATASET_FILE ->', ns.get('DATASET_FILE'))
print('DATASET exists ->', Path(ns.get('DATASET_FILE')).exists())
