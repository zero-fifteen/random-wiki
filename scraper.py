from wiki_bot import WikiBot
from wiki_requests import request_pageid_from_title

bot = WikiBot(verbose=True)

with open("categories.txt") as catsfile:
    cats = catsfile.read().splitlines()
    for idx, cat in enumerate(cats):
        catid = request_pageid_from_title("Category:" + cat)

        print(f"[{idx}/{len(cats)}] Scraping Category:{cat}...")
        try:
            subcats = bot.get_all_subcategories(catid)
            bot.save_array(cat, subcats)
        except:
            print(f">>>>>>>>>Errored out scraping Category:{cat}.")
        # print(bot.random_page(catid, save=True, regen=False, check=False))
