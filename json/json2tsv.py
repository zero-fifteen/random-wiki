import json
import csv
import glob
from collections import defaultdict

def recursive_subcats_of(catid, subcats_dict, history=None):
    if history is None:
        history = []
    else:
        yield catid
        print(f"Now processing {catid} (depth {len(history)}, {'->'.join(str(x) for x in history)})")
    history = [x for x in history] + [catid]
    if len(history) < 4:
        for subcat in subcats_dict[catid]:
            if subcat is None or subcat in history:
                print("Skipping {catid}")
            else:
                yield from recursive_subcats_of(subcat, subcats_dict, history=history)

with open("cats.tsv", "w", newline="") as tsv:
    writer = csv.writer(tsv, delimiter=',')
    fieldnames = ['catid', 'page_count', 'depth', 'parent']
    writer.writerow(fieldnames)
    for fname in glob.iglob('*.json'):
        print(fname)
        with open(fname) as jsonfile:
            these_cats = json.load(jsonfile)
        for cat, data in these_cats.items():
            tsv_data = [int(cat), data["page_count"], data["depth"], data["parent"]]
            writer.writerow(tsv_data)

with open("subcats.tsv", "w", newline="") as tsv:
    writer = csv.writer(tsv, delimiter=',')
    fieldnames = ['catid', 'page_count', 'subcats']
    writer.writerow(fieldnames)

    subcats_dict = defaultdict(list)

    for fname in glob.iglob('*.json'):
        with open(fname) as jsonfile:
            these_cats = json.load(jsonfile)
        for cat, data in these_cats.items():
            if data["parent"] is not None:
                subcats_dict[data["parent"]].append(int(cat))

    keys = subcats_dict.keys()
    full_subcats_dict = {}
    for catid in keys:
        full_subcats_dict[catid] = list(recursive_subcats_of(catid, subcats_dict))
    # full_subcats_dict = {catid: list(recursive_subcats_of(catid, subcats_dict)) for catid in keys}

    for parent, subcats in full_subcats_dict.items():
        print(parent, subcats)
