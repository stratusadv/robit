from robit import Robit

from time import sleep

rb = Robit('Epiphany Real Estate Finder')


def test_function():
    sleep(10)


rb.add_part('Test Function', test_function)

if __name__ == '__main__':
    rb.run()
