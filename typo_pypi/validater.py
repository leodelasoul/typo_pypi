'''
TODO I need to find out there patterns, how one steals either keys, mines bitcoins or uses us as a bot for their net

'''

import json
import threading
import yara
import os
from os.path import isfile, join
from typo_pypi.package import Package
import re
from typo_pypi import config
import logging

class Validater(threading.Thread):
    current_dir = os.path.dirname(__file__)

    def __init__(self, name, condition):

        super().__init__(name=name)
        self.condition = condition

    def run(self):
        while config.run:
            self.condition.acquire()
            if config.tmp_file != "":
                config.suspicious_package = self.check_sig_discription(config.tmp_file)
                self.condition.notify_all()
                if config.file_isready:
                    self.classify_package(config.suspicious_dir)
                    self.condition.notify_all()
                else:
                    pass
            else:
                self.condition.wait()
            self.condition.release()

    def check_sig_discription(self, data):
        rules = yara.compile(self.current_dir + "/yara/pypi.yara")
        match = rules.match(data)
        if match:
            check = True
        else:
            check = True
        return check

    def classify_package(self, suspicious_dir):
        # check content of file
        config.file_isready = False  # for next iteration
        '''rules = yara.compile(filepaths={
    "setup": "./yara/setup.yara",
    "MD5_Constants": "./yara/crypto.yara",
    "Big_Numbers0': './yara/crypto.yara",
    "Big_Numbers0': './yara/crypto.yara"

}) '''
        rules = yara.compile(filepath="./yara/crypto.yara")


        package_obj = Package(config.real_package)
        package_obj[0] = config.typo_package
        try:

            for file in [f for f in os.listdir(suspicious_dir) if isfile(join(suspicious_dir, f)) and f.endswith("py")]: #and not f.endswith("json")
                match = rules.match(suspicious_dir + file)
                # true positive : harmful = true , false positive: should be excluded, , true negative: squatt = true, false negative: not considered further as typo
                if match:
                    package_obj.harmful = True
                    package_obj.namesquat = False
                    logging.warning("harmful code for namespace: " + package_obj.typos[0] + " \n" + "in source file: " + file)
                    break

                else:
                    package_obj.namesquat = True
                    package_obj.harmful = False

                    continue
        except Exception as e:
            print(e)
            return
