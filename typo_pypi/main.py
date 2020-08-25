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

def main():
    try:
        threads = []
        tmp_dir = tempfile.mkdtemp(prefix="typo_pypi")

        analizer = Analizer()
        server = Server(tmp_dir)
        validater = Validater()

        analizer.start()
        time.sleep(2)
        threads.append(analizer)
        server.start()
        threads.append(server)
        validater.start()
        time.sleep(2)
        threads.append(validater)

        print("threads started")
        # class methods should execute
        for thread in threads:
            thread.join()
    finally:
        try:
            shutil.rmtree(tmp_dir)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise  # re-raise exception



if __name__ == '__main__':
    main()