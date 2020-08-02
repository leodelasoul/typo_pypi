import json
from typo_pypi.package import Package

from typo_pypi.algos import Algos


class Analizer:
    package_list = list()
    with open("./../top-pypi-packages-30-days.json", "r") as file:
        data = json.load(file)
        for p in data["rows"]:
            obj = Package(p["project"], p["download_count"], Algos.generate_typo(p["project"]))
            package_list.append(obj)


    print(Algos.hamming_distance("abc", "yxz"))


