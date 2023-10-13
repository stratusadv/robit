import random
from time import sleep

import robit


robit.set_utc_offset(-6)


def function_to_alert_me(**kwargs):
    print(f"{kwargs['alert_message']}")


wo = robit.Worker(
    name='Robit Example Worker',
    key='Your-Own-Unique-Worker-Key-That-Is-Secure',
    web_server=True,
    # web_server_address='0.0.0.0',
    # web_server_port=8000,
    # alert_method=function_to_alert_me,
    # alert_health_threshold=99.0,
)


def function_sleep_short():
    sleep(2)
    return 'Slept for 2 seconds'


def function_sleep_for_time(sleep_time: int):
    sleep(sleep_time)
    return 'Slept for 6 seconds'


wo.add_job(
    'Specific Sleep Period Function',
    function_sleep_for_time,
    method_kwargs={'sleep_time': 12},
    group='Sleeping',
    cron='* * * * *'
)

wo.add_job(
    'Sleep 3 Seconds Function Every 5 Seconds',
    function_sleep_for_time,
    method_kwargs={'sleep_time': 3},
    group='Sleeping',
    cron='*/5 * * * * *'
)

wo.add_job(
    'Sleep for Short Period',
    function_sleep_short,
    group='Sleeping',
    cron='*/2 * * * *'
)


def function_random_fail_often():
    # if 1 == random.randint(1,2):
    division_by_zero = 5 / 0
    sleep(4)
    return 'No Error'


def function_random_fail_rare():
    if 1 == random.randint(1,20):
        division_by_zero = 5 / 0
    sleep(4)
    return 'No Error'


wo.add_job(
    'A Function that Fails',
    function_random_fail_often,
    group='Failing',
    cron='* * * * *'
)

wo.add_job(
    'Might Fail Some Times',
    function_random_fail_rare,
    group='Failing',
    cron='* * * * *'
)


def function_full_speed():
    x = int()
    for i in range(100000):
        x = i * i
    sleep(1)
    return f'Max multiplication result of {x:,}'


wo.add_job('Lower Delay Function', function_full_speed, group='Rapid Execution', cron='* * * * * *')


if __name__ == '__main__':
    wo.start()
