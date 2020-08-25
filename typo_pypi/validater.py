'''
TODO I need to find out there patterns, how one steals either keys, mines bitcoins or uses us as a bot for their net

'''

import json
import threading

import yara
import tarfile
import os
import re

class Validater(threading.Thread):
    current_dir = os.path.dirname(__file__)


    def __init__(self):
        super().__init__()

    def run(self):
        self.test()
        #incluse here the check disript
        #include here the setup.py check

    def test(self):
        print("validater executes stuff now!")

    def check_sig_discription(self, data):
        check = False
        rules = yara.compile(self.current_dir + "/yara/pypi.yara")
        match = rules.match(data)
        if match:
            print("hit")
            check = True
        return check

    def validate_package(self, setup_file):
        # prüfe inhalt des downloads mittels yara
        rules = yara.compile(filepaths={
            'Big_Numbers0': './yara/crypto.yara',
            'fragus_htm': './yara/fragus.yara'
        })
        try:
            package_source = open(setup_file)
        except Exception:
            return
        else:
            rules.match(package_source)

    def extract_setup_file(self, downloaded_file):
        print(downloaded_file)
        try:
            dest = re.match(r".*\\([^\\]+)/", downloaded_file)
            dest1 = re.match(r".*/([^//]+)/", downloaded_file)
        except TypeError as e:
            return

        try:
            t = tarfile.open(downloaded_file, 'r')
        except tarfile.ReadError as e:
            print(e)
        else:
            for member in t.getmembers():
                if "setup.py" in member.name:
                    if os.name == "posix":
                        t.extract(member, dest1[0])

                    elif os.name == "nt":
                        t.extract(member, dest[0])
