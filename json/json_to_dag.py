import json
import glob
from collections import defaultdict

all_cats = defaultdict(list)
for fname in glob.iglob('*.json'):
    with open(fname) as jsonfile:
        these_cats = json.load(jsonfile)
    for cat, data in these_cats.items():
        all_cats[cat].append(data)

ranked_cats = dict()
for k, v in all_cats.items():
    ranked_cats[k] = v[0]
    ranked_cats[k]['parent'] = [str(v[0]['parent'])]

    if len(v) > 1:
        min_depth = min(d['depth'] for d in v)
        ranked_cats[k]['depth'] = min_depth
        parents = set()
        for entry in v:
            if entry['depth'] == min_depth:
                parent = entry['parent']
                if isinstance(parent, list):
                    parents.update(str(x) for x in entry['parent'] if x is not None)
                elif parent is None:
                    pass
                else:
                    parents.add(str(entry['parent']))
        ranked_cats[k]['parent'] = list(parents)

with open("ranked_cats.json", "w", newline="") as outjson: 
    json.dump(ranked_cats, outjson, sort_keys=True, indent=2)
