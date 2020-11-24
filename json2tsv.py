import json
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


if __name__ == '__main__':
    subcats_dict = defaultdict(list)

    with open("ranked_cats.json") as jsonfile:
        these_cats = json.load(jsonfile)

    for cat, data in these_cats.items():
        for parent in data["parent"]:
            subcats_dict[parent].append(cat)

    keys = [k for k in subcats_dict.keys()]
    full_subcats_dict = {}
    for catid in keys:
        full_subcats_dict[catid] = list(recursive_subcats_of(catid, subcats_dict))

    with open("all_subcats.json", "w") as outfile:
        json.dump(full_subcats_dict, outfile, sort_keys=True, indent=2)
