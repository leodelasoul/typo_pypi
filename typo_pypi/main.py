import time
import threading
from typo_pypi.validater import Validater
from typo_pypi.analizer import Analizer
from typo_pypi.server import Server
import tempfile
import shutil
import errno

'''
entry point of experiment
'''


def execute_analizer():  # expandable for other indices
    Analizer()
    time.sleep(2)


def execute_server(arg):
    server = Server(arg)
    server.query_pypi_index()
    time.sleep(2)


def execute_validater():
    Validater()
    time.sleep(2)


if __name__ == '__main__':
    try:
        tmp_dir = tempfile.mkdtemp(prefix="typo_pypi")
        threads = list()
        x = threading.Thread(target=execute_analizer)
        y = threading.Thread(target=execute_server(tmp_dir))
        z = threading.Thread(target=execute_validater())
        threads.append(x)
        threads.append(y)
        threads.append(z)
        x.start()
        y.start()
        z.start()
        print("threads started")
        x.join()
        y.join()
        z.join()
    finally:
        try:
            shutil.rmtree(tmp_dir)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise  # re-raise exception
