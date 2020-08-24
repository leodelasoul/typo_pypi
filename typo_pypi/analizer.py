import json
import threading

from typo_pypi.package import Package

from typo_pypi.algos import Algos

'''
use to generate lists for different indices

'''


class Analizer(threading.Thread):
    package_list = list()

    def __init__(self):
        super().__init__()

    def run(self):
        with open("./../top-pypi-packages-30-days.json", "r") as file:
            data = json.load(file)
            for p in data["rows"]:
                obj = Package(p["project"], p["download_count"], Algos.generate_typo(p["project"]))
                self.package_list.append(obj)

    print(Algos.hamming_distance("abc", "yxz"))
