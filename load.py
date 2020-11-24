import json

from app import db, Category, CatLink

db.drop_all()
db.create_all()

print("Migrating Categories...")
with open("ranked_cats.json") as jsonfile:
    js = json.load(jsonfile)
    db.session.add_all(Category(pageid=int(k), pagecount=v['page_count'])
                       for k, v in js.items())

print("Migrating CatLinks...")
with open("all_subcats.json") as jsonfile:
    js = json.load(jsonfile)
    db.session.add_all(CatLink(parent_id=int(k), child_id=int(c))
                       for k, v in js.items()
                       if k != 'None'
                       for c in set(v))

print("Committing...")
db.session.commit()
