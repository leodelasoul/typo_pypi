'''
TODO scrape Packages for their setup.py content, or download them and read their lines.
TODO I need to find out there patterns, how one steals either keys, mines bitcoins or uses us as a bot for their net




'''

import json


class Validater:
    with open('results.json', encoding="utf-8") as f:
        packages_to_validate = json.load(f)


