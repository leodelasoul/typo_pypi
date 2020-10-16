'''
TODO I need to find out there patterns, how one steals either keys, mines bitcoins or uses us as a bot for their net

'''

import json
import threading
import yara
import os
from typo_pypi.package import Package
import re
from typo_pypi import config


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
            elif config.setup_file != "" or config.setup_file != None:
                self.classify_package(config.setup_file)
                self.condition.notify_all()
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

    def classify_package(self, setup_file):
        # check content of file
        rules = yara.compile(filepaths={
            "setup": "./yara/setup.yara"
            # 'Big_Numbers0': './yara/crypto.yara',
            # 'fragus_htm': './yara/fragus.yara'
        })
        package_obj = Package(config.real_package)
        package_obj[0] = config.typo_package
        try:
            match = rules.match(setup_file)
        except Exception:

            return
        else:
            # true positive : harmful = true , false positive: should be excluded, , true negative: squatt = true, false negative: not considered further as typo
            if match:
                package_obj.harmful = True
                print("hit on : " + package_obj.typos[0])

            else:
                package_obj.namesquat = True
                print("nothing on : " + package_obj.typos[0])
