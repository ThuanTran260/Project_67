import pandas as pd
import json

csv=r'e:\\Bao Cao Ha Dung\\Tuan 2\\Project\\results\\comparison_3sets.csv'
j=r'e:\\Bao Cao Ha Dung\\Tuan 2\\Project\\data\\processed\\hidden_v2.json'

df=pd.read_csv(csv)
with open(j,'r',encoding='utf-8') as f:
    tasks=json.load(f)

hmap={t['task_id']:t['topic'] for t in tasks}
csvmap={int(r['task_id']):r['topic'] for _,r in df.iterrows()}

for topic in ['list','math','string']:
    h={tid for tid,top in hmap.items() if top==topic}
    c={tid for tid,top in csvmap.items() if top==topic}
    print(topic, 'hidden', len(h), 'csv', len(c))
    print(' only_in_hidden', sorted(h-c))
    print(' only_in_csv', sorted(c-h))
    print()

# Sanity check: compare total counts and task_ids
print('hidden task_ids count:', len(hmap))
print('csv task_ids count:', len(csvmap))

# print topic lists for manual inspection if needed
#print('hidden topics per id:', hmap)
#print('csv topics per id:', csvmap)
