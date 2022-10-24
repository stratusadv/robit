import random
from time import sleep

from robit import Worker


def function_to_alert_me(**kwargs):
    print(f"{kwargs['alert_message']}")


wo = Worker(
    name='Robit Example Worker',
    key='Your-Own-Unique-Worker-Key-That-Secure',
    web_server=True,
    web_server_address='0.0.0.0',
    # web_server_port=8000,
    monitor_address='http://127.0.0.1192.:8200',
    monitor_key='Your-Own-Unique-Monitor-Key-That-Secure',
    utc_offset=-7,
    # alert_method=function_to_alert_me,
    # alert_health_threshold=99.0,
)


def function_sleep_short():
    sleep(2)
    return 'Slept for 2 seconds'


def function_sleep_for_time(sleep_time: int):
    sleep(sleep_time)
    return 'Slept for 6 seconds'


wo.add_job('Sleep for Short Period', function_sleep_short, group='Sleeping', cron='0 6 * * 1')
wo.add_job('Specific Sleep Period Function', function_sleep_for_time, method_kwargs={'sleep_time': 6}, group='Sleeping')


def function_random_fail_often():
    if 1 == random.randint(1,2):
        division_by_zero = 5 / 0
    sleep(4)
    return 'No Error'


def function_random_fail_rare():
    if 1 == random.randint(1,20):
        division_by_zero = 5 / 0
    sleep(4)
    return 'No Error'


wo.add_group('Failing', alert_method=function_to_alert_me, alert_health_threshold=99.0)

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
