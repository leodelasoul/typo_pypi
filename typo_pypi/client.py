import threading

import requests
from collections import defaultdict
from typo_pypi.analizer import Analizer
import json
# from typo_pypi.validater import Validater
import os
from typo_pypi import config
import tarfile
import re
import logging

'''
gets packages by https, downloads and extracts it as a thread 

'''


class Client(threading.Thread):
    idx = 0
    data = defaultdict(list)
    typos = list()
    url = ""

    def __init__(self, name, tmp_dir, condition):
        super().__init__(name=name)
        self.tmp_dir = tmp_dir  # store tmp data
        self.condition = condition
        self.iter = iter(list())

    def get_last_element(self):
        return self.typos[-1]

    with open(os.path.dirname(__file__) + "/blacklist.json") as f:
        blacklist = json.load(f)

    def run(self):

        while config.run:
            self.query_list()

    def query_list(self):

        def to_json_file(package, typo):
            info = typo.json()["info"]
            self.typos.append(info)
            self.data[package].append(self.get_last_element())

        try:
            lines = config.package_list
            line = json.loads(lines[self.idx])  # aka next line
        except Exception:
            pass
        else:
            config.predicate_flag = False
            line = json.loads(lines[self.idx])  # aka next line
            x = requests.get("https://pypi.org/pypi/" + line['p_typo'] + "/json")
            if x.status_code == 200 and x.json()["info"]['author_email'] not in Client.blacklist['authors'] and \
                    line["p_typo"] not in Client.blacklist['packages']:
                self.condition.acquire()
                print(("https://pypi.org/project/" + line['p_typo']))
                t = line["p_typo"]
                to_json_file(line["real_project"], x)
                try:
                    os.mkdir(self.tmp_dir + "/" + t)
                except FileExistsError as e:
                    print(e)
                    self.condition.notify_all()
                    pass
                tmp_file = self.tmp_dir + "/" + t + "/" + t + ".json"
                config.tmp_file = tmp_file
                config.real_package = line["real_project"]
                config.typo_package = t
                self.condition.notify_all()
                with open(tmp_file, "w+", encoding="utf-8") as f:
                    json.dump({"rows": x.json()}, f, ensure_ascii=False, indent=3)
                self.condition.wait()  # validater needs to check sig first
                if config.suspicious_package:
                    self.condition.wait()
                    tar_file = self.download_package(x, t)
                    config.suspicious_dir = self.extract_setup_file(tar_file)
                    config.file_isready = True
                    self.condition.notify_all()
                    self.condition.wait_for(self.predicate)

                    self.write_results(line)
                else:

                    self.condition.notify_all()
                    pass
                self.condition.release()

            else:
                pass
            if self.idx == len(lines) - 1 and len(lines) > 10:  # exit condition with a 10 offset
                config.run = False

            self.idx = self.idx + 1


    def write_results(self,line):
        with open("results2.txt", "a") as file:
            line["namesquat"] = config.current_package_obj.namesquat
            line["harmful"] = config.current_package_obj.harmful
            json.dump(line, file)
            file.write("\n")

    def predicate(self):
        return config.predicate_flag

    def download_package(self, x, typo_name):
        try:
            key = list(x.json()["releases"].keys())[-1]
        except IndexError as e:
            print(e)
            return
        else:

            for i in range(len(x.json()["releases"][key])):
                if x.json()["releases"][key][i]["packagetype"] == "sdist":
                    self.url = x.json()["releases"][key][i]["url"]
                else:
                    continue
            try:
                data = requests.get(self.url, stream=True)
            except Exception:
                return
            else:
                out_file = self.tmp_dir + "/" + typo_name + "/" + typo_name + '.tar.gz'
                with open(out_file, 'wb') as fp:
                    for chunk in data.iter_content():
                        if chunk:
                            fp.write(chunk)
                            fp.flush()
                return out_file

    def extract_setup_file(self, downloaded_file):
        destination = ""
        logging.info("extracted : " + str(config.typo_package))
        try:
            dest = re.match(r".*\\([^\\]+)/", downloaded_file)
            dest1 = re.match(r".*/([^//]+)/", downloaded_file)
        except Exception as e:
            print("no extractable file found: " + str(e))
            return None
        try:
            t = tarfile.open(downloaded_file, 'r')
        except tarfile.ReadError as e:
            print(str(e) + "; packaged falsely")
            return None
        else:
            for member in t.getmembers():
                if os.path.splitext(member.name)[1] == ".py":
                    if os.name == "posix":
                        t.extractall(path=dest1[0], members=self.members(member))
                        destination = dest1[0]

                    elif os.name == "nt":
                        t.extractall(path=dest[0], members=self.members(member))
                        destination = dest[0]

            return destination

    def members(self, member):
        match = re.match(r"^(.*[\\\/])", member.path)
        l = len(match[0])
        if member.path.startswith(config.typo_package):
            member.path = member.path[l:]
            yield member
