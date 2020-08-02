import requests
from typo_pypi.analizer import Analizer
import json


with open('blacklist.json') as f:
    blacklist = json.load(f)


def query_pypi_index():
    for p in Analizer.package_list:
        for t in p.typos:
            x = requests.get("https://pypi.org/pypi/" + t + "/json")
            if x.status_code == 200 and x.json()["info"]['author_email'] not in blacklist['authors']:
                p.set_check(True)
                print(("https://pypi.org/project/" + t))
                f = open('typo_packages_unequal_len_black.txt', 'a')
                f.write("https://pypi.org/project/" + t + '\n')
            else:
                p.set_check(False)



query_pypi_index()


#x = requests.get("https://pypi.org/pypi/trafaretconfig/json")
                  #https://pypi.org/pypi/trafaretconfig/json
#print(x.json()["info"]['author_email'])