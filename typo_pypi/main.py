import time
import threading

from validater import Validater
from analizer import Analizer
from client import Client
import config
#---- dist packages
import logging.handlers
import os
import threading
import tempfile
import shutil
import errno
import logging
import sys
'''
entry point of experiment
'''
c = threading.Condition()


def main():
    logging.basicConfig(level=logging.INFO, filename= "typo_pypi.log")
    should_roll_over = os.path.isfile("typo_pypi.log")
    handler = logging.handlers.RotatingFileHandler("typo_pypi.log", mode='w', backupCount=0)
    results = logging.handlers.RotatingFileHandler("results2.txt", mode='w', backupCount=0)
    try :
        samplesize = sys.argv
        config.samplesize = samplesize[1]
    except IndexError:
        print("specify a samplesize in range of 0-3999")
        return

    if should_roll_over:  # log already exists, roll over!
        handler.doRollover()
        results.doRollover()
        pass
    try:
        threads = []
        tmp_dir = tempfile.mkdtemp(prefix="typo_pypi")
        analizer = Analizer("analizerthread",c)
        client = Client("clientthread", tmp_dir, c)
        validater = Validater("validaterhtread", c)

        analizer.start()
        threads.append(analizer)
        threads.append(client)
        threads.append(validater)
        client.start()
        validater.start()

        logging.info('threads started')
        # class methods should execute
        for thread in threads:
            thread.join()
            time.sleep(1)
    finally:
        try:
            shutil.rmtree(tmp_dir)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise  # re-raise exception


if __name__ == '__main__':
    now = time.time()
    main()
    later = time.time()
    logging.info("elapsed time: " + str(later - now))