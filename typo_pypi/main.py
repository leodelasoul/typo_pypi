
import time
import threading


def execute_analizer():
    import typo_pypi.analizer
    time.sleep(2)

def execute_server():
    import typo_pypi.server
    time.sleep(2)


if __name__ == '__main__':

    threads = list()
    x = threading.Thread(target=execute_analizer)
    y = threading.Thread(target=execute_server)
    threads.append(x)
    threads.append(y)
    x.start()
    y.start()

    print("threads started")

    x.join()
    y.join()