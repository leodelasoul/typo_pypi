from typo_pypi.package import Package

idx = 0
json_data = None
tmp_file = ""
suspicious_dir = ""
suspicious_package = False
run = True

real_package = ""
typo_package = ""
file_isready = False
current_package_obj = Package("")

package_list = list()

predicate_flag_validator = False
predicate_flag_analizer = False
