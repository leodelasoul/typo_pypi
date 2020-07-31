import requests
from typo_pypi.analizer import Analizer

for p in Analizer.package_list:
    x = requests.get("https://pypi.org/project/" + p.project)
    if(x.status_code == 200):
        p.set_check(True)
        print("Hit")

    else:
        p.set_check(False)
        print("Miss")
