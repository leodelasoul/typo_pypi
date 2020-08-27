import threading

import requests
from collections import defaultdict
from typo_pypi.analizer import Analizer
import json
from typo_pypi.validater import Validater
import os



'''
manages all http requests that are needed for  this project

'''


class Server(threading.Thread):

    def __init__(self, tmp_dir):
        super().__init__()
        self.tmp_dir = tmp_dir  # store tmp data

    with open(os.path.dirname(__file__) + "/blacklist.json") as f:
        blacklist = json.load(f)

    def run(self):
        #self.query_pypi_index()
        pass

    def query_pypi_index(self):
        data = defaultdict(list)
        typos = list()
        validater = Validater()

        def to_json_file(package, typo, idx):
            nonlocal data
            nonlocal typos
            info = typo.json()["info"]
            typos.append(info)
            data[package].append(typos[idx])
            return data
        idx = 0
        for i, p in enumerate(Analizer.package_list):
            if i == 10:  # for dev purpose only
                break
            for t in p.typos:
                x = requests.get("https://pypi.org/pypi/" + t + "/json")
                if x.status_code == 200 and x.json()["info"]['author_email'] not in Server.blacklist['authors']:
                    p.set_check(True)
                    print(("https://pypi.org/project/" + t))
                    data = to_json_file(p.project, x, idx)
                    os.mkdir(self.tmp_dir + "/" + t)
                    tmp_file = self.tmp_dir + "/" + t + "/" + t + ".json"
                    with open(tmp_file, "w+", encoding="utf-8") as f:
                        json.dump({"rows": data}, f, ensure_ascii=False, indent=3)
                    if validater.check_sig_discription(tmp_file):
                        tar_file = self.download_package(x, t)
                        setup_file = validater.extract_setup_file(tar_file)
                        #validater.validate_package(setup_file)
                    idx = idx + 1
                else:
                    p.set_check(False)

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

    # y = requests.get("https://pypi.org/pypi/trafaretconfig/json")
    # x = list(y.json()["releases"][x][0]["url"]n()["releases"].keys())[0]
    # print(type(x))
    # print()
