import time
import threading

from typo_pypi.validater import Validater
from typo_pypi.analizer import Analizer
from typo_pypi.server import Server
from typo_pypi.algos import Algos
import threading
import tempfile
import shutil
import errno

'''
entry point of experiment
'''


def main():
    c = threading.Condition()

    try:
        threads = []
        tmp_dir = tempfile.mkdtemp(prefix="typo_pypi")
        analizer = Analizer()
        server = Server("serverthread", tmp_dir,c)
        validater = Validater("validaterthread",c)

        analizer.start()
        time.sleep(2)
        threads.append(analizer)
        threads.append(server)
        validater.start()
        threads.append(validater)
        #time.sleep()
        server.start()

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
