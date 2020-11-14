from flask import Flask, redirect
import requests as r 
from requests.exceptions import TooManyRedirects
# import wikipediaapi as wiki
from random import random

import re

app = Flask(__name__)

@app.route('/<category>')
def redirect_to_category(category, depth=0, breadcrumbs=[]):
    url = f"https://en.wikipedia.org/wiki/Special:RandomInCategory/{category}"
    if depth > 10:
        raise TooManyRedirects()
    
    resolved_url = r.get(url).url
    # Test if this itself is a special page
    special_match = re.match("https://en.wikipedia.org/wiki/([^:]+):(.+)", resolved_url)
    if special_match:
        special_type = special_match.group(1)
        special_keyword = special_match.group(2)
        print(f"found special match {special_type}:{special_keyword}")

        if special_type == "Book":
            print(f"")
            return
        elif special_type == "Category":
            print(f"recursing on category {special_keyword}")
            breadcrumbs.append(special_keyword.replace("_", " "))
            return redirect_to_category(special_keyword, depth=depth+1, breadcrumbs=breadcrumbs)
        else:
            print(f"don't know what to do with this, retrying with category {category}...")
            return redirect_to_category(category, depth=depth+1, breadcrumbs=breadcrumbs)
    else:
        if random() < (0.5 ** (depth + 1)):
            print(f"don't like this page, trying again with category {category}...")
            return redirect_to_category(category, depth=depth+1, breadcrumbs=breadcrumbs)

        print(" > ".join(breadcrumbs))
        breadcrumbs = []
        return redirect(resolved_url)

