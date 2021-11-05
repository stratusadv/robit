import random
from time import sleep

from robit import Worker

# To connect to an active monitor use monitor_address & monitor_key
# wo = Worker('Robit Example Worker', key='Your-Own-Unique-Worker-Key-That-Secure', monitor_address='http://127.0.0.1:8200', monitor_key='Your-Own-Unique-Monitor-Key-That-Secure')
wo = Worker('Robit Example Worker', web_server_address='0.0.0.0', key='Your-Own-Unique-Worker-Key-That-Secure')
# wo = Worker('Robit Example Worker', key='Your-Own-Unique-Worker-Key-That-Secure', web_server=False)


def function_sleep_short():
    sleep(2)
    return 'Slept for 2 seconds'


def function_sleep_for_time(sleep_time: int):
    sleep(sleep_time)
    return 'Slept for 6 seconds'


wo.add_job('Sleep for Short Period', function_sleep_short, group='Sleeping', cron='10 7 * * *')
wo.add_job('Specific Sleep Period Function', function_sleep_for_time, method_kwargs={'sleep_time': 6}, group='Sleeping')


def function_random_fail_often():
    if 1 == random.randint(1,3):
        division_by_zero = 5 / 0
    sleep(4)
    return 'No Error'


def function_random_fail_rare():
    if 1 == random.randint(1,30):
        division_by_zero = 5 / 0
    sleep(4)
    return 'No Error'


wo.add_job('A Function that Fails Often', function_random_fail_often, group='Failing')
wo.add_job('Might Fail Some Times', function_random_fail_rare, group='Failing')


def function_full_speed():
    x = int()
    for i in range(100000):
        x = i * i
    sleep(1)
    return f'Max multiplication result of {x:,}'


wo.add_job('Lower Delay Function', function_full_speed, group='Rapid Execution')


if __name__ == '__main__':
    wo.start()
