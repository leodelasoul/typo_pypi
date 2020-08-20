'''
TODO scrape Packages for their setup.py content, or download them and read their lines.
TODO I need to find out there patterns, how one steals either keys, mines bitcoins or uses us as a bot for their net

'''

import json
import yara

class Validater:

    def __init__(self):
        pass

    with open('results.json', encoding="utf-8") as f:
        packages_to_validate = json.load(f)

    def check_sig_discription(self, data):
        check = False
        rules = yara.compile("./yara/pypi.yara")
        match = rules.match(data)

        if match:
            check = True
        return check

    def validate_package(self):
        # prüfe inhalt des downloads mittels yara
        rules = yara.compile(filepaths={
            'Big_Numbers0': './yara/crypto.yara',
            'fragus_htm': './yara/fragus.yara'
        })
        package_source = open("some file within dir structure")
        rules.match(package_source)

        return


