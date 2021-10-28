from robit import Worker

from time import sleep

wo = Worker('Test Worker')


def test_function():
    sleep(10)


wo.add_job('Test Function', test_function)

if __name__ == '__main__':
    wo.run()
