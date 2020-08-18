import requests
from typo_pypi.analizer import Analizer
import json


class Server:
    with open('blacklist.json') as f:
        blacklist = json.load(f)

    def query_pypi_index(self):
        data = dict()
        typos = list()

        def to_json_file(package, typo):
            nonlocal data
            nonlocal typos

            info = typo.json()["info"]
            typos.append(info)
            data[package] = typos
            return data

        for i, p in enumerate(Analizer.package_list):
            if i == 30:  # for dev purpose only
                break
            for t in p.typos:
                x = requests.get("https://pypi.org/pypi/" + t + "/json")
                if x.status_code == 200 and x.json()["info"]['author_email'] not in Server.blacklist['authors']:
                    p.set_check(True)
                    print(("https://pypi.org/project/" + t))
                    data = to_json_file(p.project, x)
                    pass
                else:
                    p.set_check(False)

        with open("results.json", "a", encoding='utf-8') as f:
            json.dump({"rows": data}, f, ensure_ascii=False, indent=3)

    # query_pypi_index()

    # x = requests.get("https://pypi.org/pypi/trafaretconfig/json")
    # https://pypi.org/pypi/trafaretconfig/json
    # print(x.json()["info"]['author_email'])
