import runpy
from pathlib import Path

# Execute src/run_baseline.py in isolated namespace to read its BASE and DATASET_FILE
ns = runpy.run_path('src/run_baseline.py')
BASE = ns.get('BASE')
DATA = ns.get('DATASET_FILE')
print('CWD:', Path.cwd())
print('BASE from run_baseline.py ->', BASE)
print('DATASET_FILE ->', DATA)
if DATA is not None:
    print('EXISTS ->', Path(DATA).exists())
else:
    print('DATASET_FILE not found in run_baseline.py globals')
