'''
TODO scrape Packages for their setup.py content, or download them and read their lines.
TODO I need to find out there patterns, how one steals either keys, mines bitcoins or uses us as a bot for their net

'''

import json
import yara
import tarfile
import glob

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
            print("hit")
            check = True
        return check

    def validate_package(self,setup_file):
        # prüfe inhalt des downloads mittels yara
        rules = yara.compile(filepaths={
            'Big_Numbers0': './yara/crypto.yara',
            'fragus_htm': './yara/fragus.yara'
        })
        package_source = open(setup_file)
        rules.match(package_source)
        return

    def extract_setup_file(self, downloaded_file):
        try:
            t = tarfile.open(downloaded_file, 'r')
        except tarfile.ReadError as e:
            print(e)
        else:
            for member in t.getmembers():
                if "setup.py" in member.name:
                    t.extract(member,)
