import json
import threading
import os
from typo_pypi.package import Package
from treelib import Tree
from treelib.exceptions import DuplicatedNodeIdError
from typo_pypi.algos import Algos

'''
use to generate lists/trees for different indices

'''


class Analizer(threading.Thread):
    package_list = list()
    current_dir = os.path.dirname(__file__)
    package_tree = Tree()

    def __init__(self, name):
        super().__init__(name=name)
        self.package_tree.create_node("Packages", "packages")

    def run(self):
        with open(self.current_dir + "/lol.json", "r") as file:
            data = json.load(file)
            for p in data["rows"]:
                typos = Algos.generate_typo(p["project"])
                obj = Package(p["project"], p["download_count"], typos)
                self.package_list.append(obj)
                self.package_tree.create_node(p["project"], p["project"], parent="packages")

        i = 0
        for p in self.package_list:
            for t in self.package_list[i].__dict__["typos"]:
                try:
                    self.package_tree.create_node(t, t, parent=p.__dict__["project"])
                except DuplicatedNodeIdError as e:
                    pass
                else:
                    continue
            i = i + 1

# print(Algos.hamming_distance("abc", "yxz"))
