import threading
from clint.textui import progress
import requests
from collections import defaultdict
from typo_pypi.analizer import Analizer
import json
# from typo_pypi.validater import Validater
import os
from typo_pypi import config
import tarfile
import re
import logging
import time

'''
gets packages by https, downloads and extracts it as a thread 

'''


class Client(threading.Thread):
    idx = 0
    data = defaultdict(list)
    typos = list()
    url = ""

    def __init__(self, name, tmp_dir, condition):
        super().__init__(name=name)
        self.tmp_dir = tmp_dir  # store tmp data
        self.condition = condition
        self.iter = iter(list())

    def get_last_element(self):
        return self.typos[-1]

    def run(self):

        while config.run:
            self.query_list()

    def query_list(self):

        def to_json_file(package, typo):
            info = typo.json()["info"]
            self.typos.append(info)
            self.data[package].append(self.get_last_element())

        try:
            lines = config.package_list
        except Exception:
            pass
        else:
            try:
                line = json.loads(lines[self.idx])  # aka next line
            except IndexError:
                return
            try:
                x = requests.get("https://pypi.org/pypi/" + line['p_typo'] + "/json", timeout=1)
            except requests.exceptions.Timeout:
                self.idx = self.idx + 1
            else:
                if x.status_code == 200:
                    self.condition.acquire()
                    config.idx = self.idx
                    if not self.idx == 0:
                        self.condition.notify_all()# for any waiting thread but not first iteration
                    print(("https://pypi.org/project/" + line['p_typo']))
                    t = line["p_typo"]
                    to_json_file(line["real_project"], x)
                    try:
                        os.mkdir(self.tmp_dir + "/" + t)
                    except FileExistsError as e:
                        print(e)
                        pass
                    tmp_file = self.tmp_dir + "/" + t + "/" + t + ".json"
                    config.tmp_file = tmp_file
                    config.json_data = x.json()
                    config.real_package = line["real_project"]
                    config.typo_package = t
                    tar_file = self.download_package(x, t)
                    config.suspicious_dirs.append(self.extract_setup_file(tar_file))
                    self.condition.wait()
                    print(str(config.current_package_obj.project) + "<-- from client")

                    if config.current_package_obj.typosquat or  config.current_package_obj.harmful:
                        self.condition.wait_for(self.predicate_validator)
                        self.write_results(line)# here get the current line from vali
                    else:
                        logging.info("nothing suspicious here:" + t)
                    self.condition.notify_all()
                    self.condition.release()
                else:
                    config.package_list.pop(self.idx)
                    self.idx = self.idx - 1 #skip
                if self.idx == len(lines):
                    pass
                    #config.run = False
                self.idx = self.idx + 1
            if self.idx == len(lines) and config.limit == True:
                config.run = False


    def write_results(self,line):
        with open("results2.txt", "a") as file:
            line["typosquat"] = config.current_package_obj.typosquat
            line["namesquat"] = config.current_package_obj.namesquat
            line["harmful"] = config.current_package_obj.harmful
            line["mal_code_file"] = config.current_package_obj.found_mal_code
            json.dump(line, file)
            file.write("\n")

    def predicate_validator(self):
        config.client_waiters = self.condition._waiters
        return config.predicate_flag_validator
    def predicate_analizer(self):
        return config.predicate_flag_analizer

    def download_package(self, x, typo_name):
        try:
            key = list(x.json()["releases"].keys())[-1]
        except IndexError as e:
            print(e)
            return
        else:

            for i in range(len(x.json()["releases"][key])):
                if x.json()["releases"][key][i]["packagetype"] == "sdist":
                    self.url = x.json()["releases"][key][i]["url"]
                else:
                    continue
            try:
                data = requests.get(self.url, stream=True, timeout=2)
                data.raise_for_status()
            except Exception:
                print("test")
                return
            else:
                out_file = self.tmp_dir + "/" + typo_name + "/" + typo_name + '.tar.gz'
                size = 0
                total_length = int(data.headers.get('content-length'))
                with open(out_file, 'wb') as fp:
                    for chunk in progress.bar(data.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                        if chunk:
                            #if time.time() - start > 10:
                            size += len(chunk)
                            if size > 5 * 1048576: #5 * 2^20 -> 5mb
                                print('response too large')
                                fp.flush()
                                break

                            fp.write(chunk)
                            fp.flush()
                print("download rdy")
                return out_file

    def extract_setup_file(self, downloaded_file):
        destination = ""
        #logging.info("extracted : " + str(config.typo_package))
        try:
            dest = re.match(r".*\\([^\\]+)/", downloaded_file)
            dest1 = re.match(r".*/([^//]+)/", downloaded_file)
        except Exception as e:
            print("no extractable file found: " + str(e))
            return None
        try:
            t = tarfile.open(downloaded_file, 'r')
            t.getmembers()
        except (tarfile.ReadError,EOFError) as e:
            if e == tarfile.ReadError:
                print(str(e) + "; packaged falsely")
            else:
                print(str(e) + "; sizelimit reached before")
            return None
        else:
            for member in t.getmembers():
                if os.path.splitext(member.name)[1] == ".py":
                    if os.name == "posix":
                        try:
                            t.extractall(path=dest1[0], members=self.members(member))
                        except (PermissionError,KeyError):
                            pass
                        destination = dest1[0]

                    elif os.name == "nt":
                        try:
                            t.extractall(path=dest[0], members=self.members(member))
                        except (PermissionError,KeyError):
                            pass
                        destination = dest[0]
            return destination

    def members(self, member):
        match = re.match(r"^(.*[\\\/])", member.path)
        l = len(match[0])
        if member.path.startswith(config.typo_package):
            member.path = member.path[l:]
            yield member
