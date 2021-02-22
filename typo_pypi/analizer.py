import json
import threading
import os
from package import Package
from treelib import Tree
from algos import Algos

from functools import lru_cache
import config
import logging
'''
use to generate lists/trees for different indices

'''


class Analizer(threading.Thread):
    # hash_table = [None] * (250421)  # len of all our packages

    # package_list = list()
    current_dir = os.path.dirname(__file__)
    def __init__(self, name, condition):
        super().__init__(name=name)
        self.condition = condition


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
        arr1 = []
        i = 0
        with open(Analizer.current_dir + "/../bq-results-20200913-185937-p7wc4g8anuwo.json", "rb") as file1:
            for line in file1:
                potential_typo = json.loads(line)
                value = potential_typo["name"]
                array[i] = value.lower()
                i = i + 1
        file1.close()
        return array

    def create_arr_without_spec_chars(self, all_packages_array):
        '''used to prove a specific hypothesis in chapter 7.3 where rubygems countermeasures is applied for typosquatting attacks '''
        for i,package in enumerate(all_packages_array):
            char_with_minus_at = package.find("-")
            char_with_under_at = package.find("_")
            if not char_with_minus_at == -1:
                all_packages_array[i] = package.replace("-","")
            elif not char_with_under_at == -1:
                all_packages_array[i] = package.replace("_","")
        return all_packages_array

    def compare(self,all_packages_array):
        '''used to prove a specific hypothesis in chapter 7.3 where rubygems countermeasure is applied for typosquatting attacks '''
        results = []
        used_typos = []
        with open("results2.txt", "r") as file:
            for line in file:
                p = json.loads(line)["p_typo"]
                if "-" in p:
                    p = p.replace("-","")
                    used_typos.append(p)
                    for pa in all_packages_array:
                        if p == pa:
                            results.append(p)
                elif "_" in p:
                    p = p.replace("_","")
                    used_typos.append(p)
                    for pa in all_packages_array:
                        if p == pa:
                            results.append(p)
                else:
                    continue
        results = set([x for x in results if results.count(x) > 1])
        return results


    def run(self):
            arr = [None] * (250421)
            arr = self.create_arr(arr)
            wrapper = self.lru_wrapper(arr)
            striped_arr = self.create_arr_without_spec_chars(arr)
            self.compare(striped_arr)
            idx = 0
            with open(self.current_dir + "/../top-pypi-packages-30-days.json", "r") as file:
                data = json.load(file)
                for p in data["rows"]:
                    obj = Package(p["project"])
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

