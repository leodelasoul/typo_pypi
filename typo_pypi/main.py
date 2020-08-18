
import time
import threading
from typo_pypi.validater import Validater
from typo_pypi.analizer import Analizer
from typo_pypi.server import Server
def execute_analizer():
    Analizer()
    time.sleep(2)

def execute_server():
    server = Server()
    #server.query_pypi_index()
    time.sleep(2)

def execute_validater():
    Validater()
    time.sleep(2)


if __name__ == '__main__':

    threads = list()
    x = threading.Thread(target=execute_analizer)
    y = threading.Thread(target=execute_server)
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