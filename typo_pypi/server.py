import requests
from typo_pypi.analizer import Analizer
import json

with open('blacklist.json') as f:
    blacklist = json.load(f)


def to_json_file(package, typo):
    data = dict()
    typos = list()

    info = typo.json()["info"]
    typos.append(info)
    data[package] = typos
    return data

def query_pypi_index():
    for i,p in enumerate(Analizer.package_list):
        if i == 1:   #for dev purpose only
            break
        for t in p.typos:
            x = requests.get("https://pypi.org/pypi/" + t + "/json")
            if x.status_code == 200 and x.json()["info"]['author_email'] not in blacklist['authors']:
                p.set_check(True)
                print(("https://pypi.org/project/" + t))
                data = to_json_file(p.project, x)
            else:
                p.set_check(False)

    with open("results.json", "a", encoding='utf-8') as f:
        json.dump({"rows": data}, f, ensure_ascii=False, indent=3)



query_pypi_index()


# x = requests.get("https://pypi.org/pypi/trafaretconfig/json")
# https://pypi.org/pypi/trafaretconfig/json
# print(x.json()["info"]['author_email'])
