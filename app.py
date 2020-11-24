import random
import re

from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
import requests as r


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@/wiki'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    pageid = db.Column(db.Integer, unique=True, nullable=False)
    pagecount = db.Column(db.Integer, nullable=False)


class CatLink(db.Model):
    __tablename__ = 'catlinks'
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.pageid'), primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('categories.pageid'), primary_key=True)


def request_title(pageid):
    params = {'action': 'query',
              'pageids': str(pageid),
              'prop': 'title',
              'format': 'json'}

    req = r.get('https://en.wikipedia.org/w/api.php', params).json()
    return req['query']['pages'][str(pageid)]['title']

def request_id(title):
    params = {'action': 'query',
              'titles': str(title),
              'prop': 'pageid',
              'format': 'json'}

    req = r.get('https://en.wikipedia.org/w/api.php', params).json()
    return int(list(req['query']['pages'].keys())[0])


@app.route('/<category>')
def random_in_category(category):
    catid = request_id(f"Category:{category}")
    cats = Category.query.filter((CatLink.parent_id == catid) &
                                 (Category.pageid == CatLink.child_id)).all()

    ids = [cat.pageid for cat in cats]
    counts = [cat.pagecount for cat in cats]

    destid = random.choices(ids, counts)[0]
    print(destid)
    destname = request_title(destid)
    print(destname)

    dest = None
    while dest is None or "/Category:" in dest.url:
        dest = r.get(f"https://en.wikipedia.org/wiki/Special:RandomInCategory/{destname}")
    return redirect(dest.url)
