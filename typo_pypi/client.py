import threading

import requests
from collections import defaultdict
from typo_pypi.analizer import Analizer
import json
#from typo_pypi.validater import Validater
import os
from typo_pypi import config
import tarfile
import re
'''
manages all http requests that are needed for  this project

'''

class Client(threading.Thread):


    def __init__(self, name, tmp_dir,condition):
        super().__init__(name=name)
        self.tmp_dir = tmp_dir  # store tmp data
        self.condition = condition

    with open(os.path.dirname(__file__) + "/blacklist.json") as f:
        blacklist = json.load(f)

    def run(self):
        #self.query_pypi_index()


        pass

    def query_pypi_index(self):
        data = defaultdict(list)
        typos = list()

        # validater = Validater(condition)

        def to_json_file(package, typo, idx):
            nonlocal data
            nonlocal typos
            info = typo.json()["info"]
            typos.append(info)
            data[package].append(typos[idx])
            return data

        idx = 0
        for i, p in enumerate(Analizer.package_list):
            if i == 20:  # for dev purpose only
                break
            for t in p.typos:
                x = requests.get("https://pypi.org/pypi/" + t + "/json")
                if x.status_code == 200 and x.json()["info"]['author_email'] not in Client.blacklist['authors']:
                    self.condition.acquire()
                    p.set_check(True)
                    print(("https://pypi.org/project/" + t))

                    data = to_json_file(p.project, x, idx)
                    os.mkdir(self.tmp_dir + "/" + t)
                    tmp_file = self.tmp_dir + "/" + t + "/" + t + ".json"
                    config.tmp_file = tmp_file
                    self.condition.notify_all()
                    with open(tmp_file, "w+", encoding="utf-8") as f:
                        json.dump({"rows": data}, f, ensure_ascii=False, indent=3)
                    self.condition.wait() # validater needs to check sig first
                    if config.current_package_valid:
                        self.condition.wait()
                        tar_file = self.download_package(x, t)
                        config.setup_file = self.extract_setup_file(tar_file)
                        self.condition.notify_all()
                    idx = idx + 1
                    self.condition.release()
                else:
                    p.set_check(False)
                    print(t)
        config.run = False
        with open("results1.json", "a", encoding='utf-8') as f:
            json.dump({"rows": data}, f, ensure_ascii=False, indent=3)

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
