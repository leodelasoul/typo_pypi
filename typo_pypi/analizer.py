import json
from typo_pypi.Package import Package

list = []



with open("./../top-pypi-packages-30-days.json", "r") as file:
    data = json.load(file)
    for p in  data["rows"]:
        obj = Package(p["download_count"],p["project"])
        list.append(obj)


print(list[0].__dict__)
#print(list[0].get_check())





