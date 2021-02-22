import json
import threading
import yara
import os
from os.path import isfile, join
from package import Package
import re
import config
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
    check = False
    idx = 0


    def __init__(self, name, condition):
        super().__init__(name=name)
        self.condition = condition

    def __init_(self):
        pass

    def run(self):

        while config.run:
            try:
                json.loads(config.package_list[self.idx])["p_typo"]
            except (TypeError, IndexError):
                pass
            self.condition.acquire()
            if config.tmp_file != "" and self.idx == config.idx:  # aka client index
                package_obj = Package(config.real_package)
                sus = self.check_sig_discription(config.json_data)
                config.current_package_obj = package_obj
                config.current_package_obj.typosquat = sus
                self.classify_package(config.suspicious_dirs)
                self.condition.notify_all()

            else:
                self.condition.wait(timeout=5)
            self.condition.release()

    def check_sig_discription(self, data):
        self.idx = self.idx + 1
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
        suspicious_dir = suspicious_dir[self.idx - 1]
        extval = ""
        extval1 = ""
        try:
            setup_file = suspicious_dir + "/setup.py"
            with open(setup_file, "r") as sfile:
                for line in sfile:
                    line = textwrap.dedent(line)
                    if line.startswith("url"):
                        extval = line
                    elif line.startswith("version"):
                        extval1 = line

        except Exception:
            extval = ""
        rules = yara.compile(filepaths={
            'look_for_ips': './yara/source_files.yara',
            'look_for_ips_and_not_whitelists': './yara/source_files.yara',
            'IP': './yara/ip.yara'
        }, externals={"external": extval, "external1" : extval1})
        config.current_package_obj.namesquat = self.is_namesquat(config.typo_package)
        try:
            for file in [f for f in os.listdir(suspicious_dir) if
                         isfile(join(suspicious_dir, f)) and f.endswith("py")]:  # and not f.endswith("json")
                match = rules.match(suspicious_dir + file)
                # print(match[0])
                if match:
                    config.current_package_obj.harmful = True
                    config.current_package_obj.found_mal_code = file
                    logging.warning(
                        "harmful code for namespace: " + config.typo_package + " \n" + "in source file: " + file)
                    break

                else:
                    config.current_package_obj.harmful = False
                    continue

            config.predicate_flag_validator = True
        except Exception as e:
            config.predicate_flag_validator = True
            print(e)

    def is_namesquat(self, typo):
        libs = stdlib_list("2.7") + stdlib_list("3.6")
        if typo in libs:
            return True
        else:
            return False


'''
        self.rules = yara.compile(filepaths={
            'Win32_Exploit_CVE20200601': './yara1/exploit/Win32.Exploit.CVE20200601.yara',
            'Win32_Infostealer_MultigrainPOS': './yara1/infostealer/Win32.Infostealer.MultigrainPOS.yara',
            'Win32_Infostealer_ProjectHookPOS': './yara1/infostealer/Win32.Infostealer.ProjectHookPOS.yara',
            'Win32_Trojan_Emotet': './yara1/trojan/Win32.Trojan.Emotet.yara',
            'Win32_Virus_Awfull': './yara1/virus/Win32.Virus.Awfull.yara'
        })

'''