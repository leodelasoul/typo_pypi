import json
import threading
import os
from typo_pypi.package import Package
from treelib import Tree
from typo_pypi.algos import Algos

from functools import lru_cache, wraps
from typo_pypi import config
import logging
'''
use to generate lists/trees for different indices

'''


class Analizer(threading.Thread):
    # hash_table = [None] * (250421)  # len of all our packages

    # package_list = list()
    current_dir = os.path.dirname(__file__)
    package_tree = Tree()

    def __init__(self, name, condition):
        super().__init__(name=name)
        self.package_tree.create_node("Packages", "packages")
        self.condition = condition


    def hash(self, key):
        hash = 0
        for i, c in enumerate(key):
            hash = (31 * hash + i) % 250421
        return hash

    def create_arr(self, array):
        i = 0
        with open(Analizer.current_dir + "/../bq-results-20200913-185937-p7wc4g8anuwo.json", "rb") as file1:
            for line in file1:
                potential_typo = json.loads(line)
                value = potential_typo["name"]
                array[i] = value.lower()
                i = i + 1
        file1.close()
        return array

    def run(self):
        arr = [None] * (250421)
        arr = self.create_arr(arr)
        wrapper = self.lru_wrapper(arr)
        idx = 0
        #config.package_list.append(json.dumps({"real_project": "foo", "p_typo": "botox"}))
        with open(self.current_dir + "/../top-pypi-packages-30-days.json", "r") as file:
            data = json.load(file)
            for p in data["rows"]:
                obj = Package(p["project"])
                # self.package_tree.create_node(p["project"], p["project"], parent="packages")
                if str(idx) == config.samplesize:
                    config.limit = True
                    logging.warning("analizer is done with typo creation for given samplesize \n sum of typos: " + str(
                        len(config.package_list)))
                    break
                for i in range(len(arr) - 1):
                    lev_distance = Algos.levenshtein(obj.project, wrapper(i))
                    if len(obj.project) <= 7:
                        THRESHOLD = 1
                    if len(obj.project) > 7:
                        THRESHOLD = 2
                    if (lev_distance <= THRESHOLD and wrapper(i) != obj.project):
                        obj.typos.append(wrapper(i))
                        data = json.dumps({"real_project": obj.project, "p_typo": wrapper(i)})
                        config.package_list.append(data) #for lines
                idx = idx + 1

        file.close()

