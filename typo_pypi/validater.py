import json
import threading
import yara
import os
from os.path import isfile, join
from typo_pypi.package import Package
import re
from typo_pypi import config
import logging

'''
gets passed data from client about packages, such as their discription,metadata and extracted file path to then look for suspicious
patterns

1. check json discription + metadata 
2. pass to client if suspiscious
3. client downloads scource files
4. validator checks these files for yara patterns , same as for 2.
'''


class Validater(threading.Thread):
    current_dir = os.path.dirname(__file__)
    conf_file_checked = False
    check = False
    idx = 0
    def __init__(self, name, condition):

        super().__init__(name=name)
        self.condition = condition

    def __init_(self):
        pass

    def run(self):
        current_package = ""
        current_list_package = ""
        while config.run:
            try:
                current_package = config.json_data["info"]["name"]
                current_list_package = json.loads(config.package_list[config.idx])["p_typo"]
            except (TypeError,IndexError):
                pass
            self.condition.acquire()
            if config.tmp_file != "" and current_package == current_list_package:
                print(config.package_list)
                config.suspicious_package = self.check_sig_discription(config.json_data)
                self.condition.notify_all()
                self.condition.wait()
                if config.file_isready:
                    self.classify_package(config.suspicious_dir)
                    self.condition.notify_all()
                    self.conf_file_checked = False
                else:
                    self.condition.wait()
                    self.conf_file_checked = False
            else:
                self.condition.wait()
            self.condition.release()

    #            else:
                #print(self.condition)
#                self.condition.wait()

            #self.condition.release()




    '''
    def check_sig_discription(self, data):
        if not self.conf_file_checked:
            rules = yara.compile(self.current_dir + "/yara/pypi.yara")
            match = rules.match(data)
            if match:
                self.check = True
                self.conf_file_checked = True
            else:
                self.check = False
                self.conf_file_checked = True
        else:
            return self.check
        return self.check
'''

    def check_sig_discription(self, data):
        if not self.conf_file_checked:
            self.idx = self.idx + 1
            # rules = yara.compile(self.current_dir + "/yara/pypi.yara")
            # match = rules.match(data)
            match = re.findall(r"('UNKNOWN')|('description': '')", str(data))
            if match:
                if len(match[1:]) > 2 or match[0]:
                    self.check = True
                    self.conf_file_checked = True
                else:
                    self.check = False
                    self.conf_file_checked = True
            else:
                self.check = False
                self.conf_file_checked = True
        else:
            return self.check
        return self.check

    def classify_package(self, suspicious_dir):
        # check content of file
        print("yolo")
        config.file_isready = False  # for next iteration
        '''rules = yara.compile(filepaths={
    "setup": "./yara/setup.yara",
    "MD5_Constants": "./yara/crypto.yara",
    "Big_Numbers0': './yara/crypto.yara",
    "Big_Numbers0': './yara/crypto.yara"

}) '''
        rules = yara.compile(filepath="./yara/source_files.yara")

        package_obj = Package(config.real_package)
        package_obj[0] = config.typo_package
        try:

            for file in [f for f in os.listdir(suspicious_dir) if
                         isfile(join(suspicious_dir, f)) and f.endswith("py")]:  # and not f.endswith("json")
                match = rules.match(suspicious_dir + file)
                # true positive : harmful = true , false positive: should be excluded, , true negative: squatt = true, false negative: not considered further as typo
                if match:
                    package_obj.harmful = True
                    package_obj.namesquat = False
                    logging.warning(
                        "harmful code for namespace: " + package_obj.typos[0] + " \n" + "in source file: " + file)
                    break

                else:
                    package_obj.namesquat = True
                    package_obj.harmful = False
                    continue

            config.current_package_obj = package_obj
            config.predicate_flag_validator = True
        except Exception as e:
            config.predicate_flag_validator = True
            print(e)



'''
    def check_sig_discription(self, data):
        if not self.conf_file_checked:
            rules = yara.compile(self.current_dir + "/yara/pypi.yara")
            match = rules.match(data)
            if match:
                self.check = True
                self.conf_file_checked = True
            else:
                self.check = False
                self.conf_file_checked = True
        else:
            return self.check
        return self.check
'''
