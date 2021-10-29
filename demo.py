from robit import Worker

from time import sleep
import random

wo = Worker('Test Worker')


def test_function_1():
    sleep(2)


def test_function_2():
    if 1 == random.randint(1,2):
        division_by_zero = 5 / 0
    sleep(2)


wo.add_job('Test Function 1', test_function_1)
wo.add_job('Test Function 2', test_function_2)

if __name__ == '__main__':
    wo.run()
