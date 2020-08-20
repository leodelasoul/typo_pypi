import requests
from typo_pypi.analizer import Analizer
import json
from typo_pypi.validater import Validater
import tempfile
'''
manages all http requests that are needed for  this project

'''


class Server:

    def __init__(self,tmp_dir):
        self.tmp_dir = tmp_dir


    with open('blacklist.json') as f:
        blacklist = json.load(f)

    def query_pypi_index(self):
        data = dict()
        typos = list()
        validater = Validater()

        def to_json_file(package, typo):
            nonlocal data
            nonlocal typos

            info = typo.json()["info"]
            typos.append(info)
            data[package] = typos
            return data

        for i, p in enumerate(Analizer.package_list):
            if i == 3:  # for dev purpose only
                break
            for t in p.typos:
                x = requests.get("https://pypi.org/pypi/" + t + "/json")
                if x.status_code == 200 and x.json()["info"]['author_email'] not in Server.blacklist['authors']:
                    p.set_check(True)
                    print(("https://pypi.org/project/" + t))
                    data = to_json_file(p.project, x)
                    #tmp_file = tempfile.gettempdir() + "/typo_pypi/" + t + ".txt"
                    tmp_file = self.tmp_dir + "/" + t + ".json"
                    with open(tmp_file,"w+") as f:
                        json.dump({"rows": data}, f, ensure_ascii=False, indent=3)
                    if validater.check_sig_discription(tmp_file):
                        # download the sourcecode if its suspicious
                        url = "https://pypi.org/project/" + t + "/#"  # PROBLEM: find exact namespace
                        data = requests.get(url, stream=True)
                        with open('pws.tar.gz', 'wb') as fp:
                            for chunk in data.iter_content():
                                if chunk:
                                    fp.write(chunk)
                                    fp.flush()
                    pass
                else:
                    p.set_check(False)

        with open("results1.json", "a", encoding='utf-8') as f:
            json.dump({"rows": data}, f, ensure_ascii=False, indent=3)


    #x = requests.get("https://pypi.org/pypi/trafaretconfig/json")
    #print(x.json()["info"])
