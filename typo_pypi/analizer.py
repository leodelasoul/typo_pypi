import json
import threading
import os
from typo_pypi.package import Package
from treelib import Tree
from typo_pypi.algos import Algos
from functools import lru_cache, wraps
from typo_pypi import config

'''
use to generate lists/trees for different indices

'''


class Analizer(threading.Thread):
    # hash_table = [None] * (250421)  # len of all our packages

    # package_list = list()
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

    def lru_wrapper(self, array=None):
        @lru_cache(maxsize=None)
        def get(idx):
            return array[idx]

        return get

    def create_arr(self, array):
        i = 0
        with open(Analizer.current_dir + "/../bq-results-20200913-185937-p7wc4g8anuwo.json", "rb") as file1:
            for line in file1:
                potential_typo = json.loads(line)
                value = potential_typo["name"]
                array[i] = value
                i = i + 1
        file1.close()
        return array

    def run(self):
        arr = [None] * (250421)
        arr = self.create_arr(arr)
        wrapper = self.lru_wrapper(arr)
        count = 0
        with open(self.current_dir + "/top-pypi-packages-30-days.json", "r") as file:
            data = json.load(file)
            for p in data["rows"]:
                if count == 3:
                    break
                obj = Package(p["project"], p["download_count"])
                # self.package_tree.create_node(p["project"], p["project"], parent="packages")
                for i in range(len(arr) - 1):
                    lev_distance = Algos.levenshtein(obj.project, wrapper(i))
                    if len(obj.project) <= 7:
                        THRESHOLD = 1
                    if len(obj.project) > 7:
                        THRESHOLD = 2
                    if (lev_distance <= THRESHOLD and wrapper(i) != obj.project):
                        obj.typos.append(wrapper(i))
                        with open("results2.txt", "a") as f:
                            # f.write({"real_project" : obj.project, "p_typo" : wrapper(i) + " \n"})
                            data = json.dumps({"real_project": obj.project, "p_typo": wrapper(i)})
                            #f.write(data + " \n")
                        f.close()
                    config.package_list.append(obj)
                #print(wrapper.cache_info())
                count = count + 1

        file.close()


# USED FOR Prevention purposes to look through
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
