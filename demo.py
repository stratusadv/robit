from robit import Worker

from time import sleep

wo = Worker('Test Worker')


def test_function_1():
    sleep(10)


def test_function_2():
    sleep(5)


wo.add_job('Test Function 1', test_function_1)
wo.add_job('Test Function 2', test_function_2)

if __name__ == '__main__':
    wo.run()
