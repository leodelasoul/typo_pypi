import json
import threading
import yara
import os
from os.path import isfile, join
from typo_pypi.package import Package
import re
from typo_pypi import config
import logging
from stdlib_list import stdlib_list
import textwrap

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
        fall_back_count = 0
        while config.run:
            try:
                current_package = config.json_data["info"]["name"]
                current_list_package = json.loads(config.package_list[self.idx])["p_typo"]
            except (TypeError, IndexError):
                pass
            self.condition.acquire()
            print(current_package + " counter from client")
            print(current_list_package + " counter from validater")
            fall_back_count = fall_back_count + 1
            print(fall_back_count)
            if config.tmp_file != "" and current_package == current_list_package:
                config.suspicious_package = self.check_sig_discription(config.json_data) # there might be some async here
                self.condition.notify_all()
                self.condition.wait()
                if config.file_isready:
                    self.classify_package(config.suspicious_dir)
                    self.condition.notify_all()
                    self.condition.wait()  # so that top if is used once
                else:
                    self.condition.wait()  # make this wait_for(client)
                fall_back_count = 0
            elif fall_back_count > 7:  # Fallback for asyncronity
                # self.idx - config.idx == 1 and len(config.client_waiters) > 0  and not config.predicate_flag_validator and
                config.predicate_flag_validator = True
                self.idx = config.idx
                #self.idx = self.idx + 1

            else:
                self.condition.wait()
            self.condition.release()



    def check_sig_discription(self, data):
        self.idx = self.idx + 1
        # rules = yara.compile(self.current_dir + "/yara/pypi.yara")
        # match = rules.match(data)
        unknown = re.findall(r"('UNKNOWN')", str(data))
        description = re.findall(r"('description': '')", str(data))
        if unknown or description:
            if len(unknown) > 2 or len(description) == 1:
                self.check = True
            else:
                self.check = False
        else:
            self.check = False
        return self.check

    def classify_package(self, suspicious_dir):
        # check content of file
        print("this dir was checked:" + str(suspicious_dir))
        config.file_isready = False  # for next iteration

        extval = ""
        #pattern = re.compile(r"setup\(([^\)]+)\)")
        try:
            setup_file = suspicious_dir + "/setup.py"
            with open(setup_file, "r") as sfile:
                for line in sfile:
                    line = textwrap.dedent(line)
                    if line.startswith("url"):
                        extval = line

                #matched = re.findall(pattern, str(lines))
        except Exception:
            extval = ""


        rules = yara.compile(filepath="./yara/source_files.yara", externals={"external": extval})
        package_obj = Package(config.real_package)
        package_obj[0] = config.typo_package
        package_obj.namesquat = self.is_namesquat(config.typo_package)
        try:

            for file in [f for f in os.listdir(suspicious_dir) if
                         isfile(join(suspicious_dir, f)) and f.endswith("py")]:  # and not f.endswith("json")
                match = rules.match(suspicious_dir + file)
                if match:
                    package_obj.harmful = True
                    package_obj.found_mal_code = file
                    logging.warning(
                        "harmful code for namespace: " + package_obj.typos[0] + " \n" + "in source file: " + file)
                    break

                else:
                    package_obj.harmful = False
                    continue

            config.current_package_obj = package_obj
            config.predicate_flag_validator = True
        except Exception as e:
            config.predicate_flag_validator = True
            print(e)

    def is_typosquat(self):
        pass

    def is_namesquat(self, typo):
        libs = stdlib_list("2.7") + stdlib_list("3.6")
        if typo in libs:
            return True
        else:
            return False


