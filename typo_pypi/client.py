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

'''
manages all http requests that are needed for  this project

'''


class Client(threading.Thread):
    idx = 0
    data = defaultdict(list)
    typos = list()

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
            return self.data

        with open("results2.txt", "r") as f:
            #if self.idx == 30 :
            #    config.run = False
            #    return
            try:
                lines = f.readlines()
                line = json.loads(lines[self.idx])  # aka next line
            except Exception:
                pass
            else:
                line = json.loads(lines[self.idx])  # aka next line
                x = requests.get("https://pypi.org/pypi/" + line['p_typo'] + "/json")
                if x.status_code == 200 and x.json()["info"]['author_email'] not in Client.blacklist['authors'] and line["p_typo"] not in Client.blacklist['packages']:
                    self.condition.acquire()
                    print(("https://pypi.org/project/" + line['p_typo']))
                    t = line["p_typo"]
                    #data = to_json_file(line["real_project"], x)
                    try:
                        os.mkdir(self.tmp_dir + "/" + t)
                    except FileExistsError as e:
                        print(e)
                        self.condition.notify_all()
                        pass
                    tmp_file = self.tmp_dir + "/" + t + "/" + t + ".json"
                    config.tmp_file = tmp_file
                    self.condition.notify_all()
                    with open(tmp_file, "w+", encoding="utf-8") as f:
                        json.dump({"rows": x.json()}, f, ensure_ascii=False, indent=3)
                    self.condition.wait()  # validater needs to check sig first
                    if config.suspicious_package:
                        self.condition.wait()
                        tar_file = self.download_package(x, t)
                        config.setup_file = self.extract_setup_file(tar_file)
                        self.condition.notify_all()
                    self.condition.release()
                else:
                    pass
                if self.idx == len(lines)-1 and len(lines) > 100:    #exit condition with a 100 offset
                    config.run = False
                    with open("results1.json", "a", encoding='utf-8') as f:
                        pass
                        #json.dump({"rows": self.data}, f, ensure_ascii=False, indent=3)
                self.idx = self.idx + 1


    def download_package(self, x, typo_name):
        try:
            key = list(x.json()["releases"].keys())[0]
            url = x.json()["releases"][key][0]["url"]
        except IndexError as e:
            print(e)
            return None
        else:
            data = requests.get(url, stream=True)
            out_file = self.tmp_dir + "/" + typo_name + "/" + typo_name + '.tar.gz'
            with open(out_file, 'wb') as fp:
                for chunk in data.iter_content():
                    if chunk:
                        fp.write(chunk)
                        fp.flush()
            return out_file

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
                        return dest1[0]

                    elif os.name == "nt":
                        t.extract(member, dest[0])
                        return dest[0]

# y = requests.get("https://pypi.org/pypi/trafaretconfig/json")
# x = list(y.json()["releases"][x][0]["url"]n()["releases"].keys())[0]
# print(type(x))
# print()
