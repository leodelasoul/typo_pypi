import time
import threading

from typo_pypi.validater import Validater
from typo_pypi.analizer import Analizer
from typo_pypi.client import Client
from typo_pypi.algos import Algos
import threading
import tempfile
import shutil
import errno

'''
entry point of experiment
'''
c = threading.Condition()


def main():
    try:
        threads = []
        tmp_dir = tempfile.mkdtemp(prefix="typo_pypi")
        analizer = Analizer("analizerthread")
        client = Client("serverthread", tmp_dir, c)
        validater = Validater("validaterthread", c)

        analizer.start()
        time.sleep(2)
        threads.append(analizer)
        threads.append(client)
        validater.start()
        threads.append(validater)
        time.sleep(2)
        client.start()

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
