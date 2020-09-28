import json
import threading
import os
from typo_pypi.package import Package
from treelib import Tree
from typo_pypi.algos import Algos
from functools import lru_cache, wraps,reduce
#from typo_pypi import config
from collections import Counter
from operator import and_


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
        count = 0
        with open(self.current_dir + "/top-pypi-packages-30-days.json", "r") as file:
            data = json.load(file)
            for p in data["rows"]:
                if count == 100:
                    break
                obj = Package(p["project"], p["download_count"])
                # self.package_tree.create_node(p["project"], p["project"], parent="packages")
                typos = Algos.generate_typo(p["project"])
                obj.typos = typos
                intersection = typos & set(arr)
                count = count +1
                if len(intersection) != 0:
                    with open("results2.txt", "a") as f:  #existent_typos
                        for i in intersection:
                            data = json.dumps({"real_project": obj.project, "p_typo": i})
                            f.write(data + " \n")
                    f.close()
                else:
                    continue


                '''
                for i in range(len(arr) - 1):
                    if obj.typos in arr:
                        with open("results2.txt", "a") as f:
                            data = json.dumps({"real_project": obj.project, "p_typo": object.typos})
                            f.write(data + " \n")
                        f.close()
                    else:
                        continue
                        
            '''
            # print(wrapper.cache_info())
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
