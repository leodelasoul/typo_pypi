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
    # hash_table = [None] * (250421-1)  # len of all our packages
    hash_table = dict()
    package_list = list()
    current_dir = os.path.dirname(__file__)
    package_tree = Tree()

    def __init__(self, name):
        super().__init__(name=name)
        self.package_tree.create_node("Packages", "packages")

    def hash(self, key):
        hash = 0
        for i, c in enumerate(key):
            hash = (31 * hash + i) % 250421
        return hash

    def create_hashtable(self):
        with open(self.current_dir + "/../bq-results-20200913-185937-p7wc4g8anuwo.json", "rb") as file1:
            for line in file1:
                potential_typo = json.loads(line)
                value = potential_typo["name"]
                key = hash(value)
                self.hash_table.update({key: value})

        file1.close()

    def run(self):
        self.create_hashtable()
        with open(self.current_dir + "/lol.json", "r") as file:
            data = json.load(file)
            for p in data["rows"]:
                obj = Package(p["project"], p["download_count"])
                self.package_list.append(obj)
                # self.package_tree.create_node(p["project"], p["project"], parent="packages")
                for k,v in self.hash_table.items():
                    lev_distance = Algos.levenshtein(obj.project, v)
                    if len(obj.project) <= 7:
                        THRESHOLD = 1
                    if len(obj.project) > 7:
                        THRESHOLD = 2
                    if (lev_distance <= THRESHOLD and v != obj.project):
                        obj.typos.append(v)
                        with open("results1.txt", "a", encoding='utf-8') as f:
                            print(v)
                            f.write(v + " \n")
                        f.close()
        file.close()

'''     i = 0
        for p in self.package_list:
            for t in self.package_list[i].__dict__["typos"]:
                try:
                    self.package_tree.create_node(t, t, parent=p.__dict__["project"])
                except DuplicatedNodeIdError as e:
                    pass
                else:
                    continue
            i = i + 1
'''

# print(Algos.hamming_distance("abc", "yxz"))
