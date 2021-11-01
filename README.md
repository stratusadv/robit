# Robit

- Lightweight (no installed dependencies) Service Worker Framework

## Usage

### Worker

- Code below is provided in the examples/worker_example.py file of this project.

```python
import random
from time import sleep

from robit import Worker

wo = Worker('Robit Example Worker', key='Your-Own-Unique-Worker-Key-That-Secure')

# To connect to an active monitor use monitor_address & monitor_key
# wo = Worker('Robit Example Worker', key='Your-Own-Unique-Worker-Key-That-Secure', monitor_address='http://127.0.0.1:8200', monitor_key='Your-Own-Unique-Monitor-Key-That-Secure')

def function_sleep_short():
    sleep(2)

def function_sleep_long():
    sleep(6)

wo.add_job('Sleep for Short Period', function_sleep_short, 'Sleeping')
wo.add_job('Longer Sleep Period Function', function_sleep_long, 'Sleeping')

def function_random_fail_often():
    if 1 == random.randint(1,3):
        division_by_zero = 5 / 0
    sleep(4)

def function_random_fail_rare():
    if 1 == random.randint(1,30):
        division_by_zero = 5 / 0
    sleep(4)

wo.add_job('A Function that Fails Often', function_random_fail_often, 'Failing')
wo.add_job('Might Fail Some Times', function_random_fail_rare, 'Failing')

def function_full_speed():
    for i in range(100000):
        x = i * i
    sleep(1)

wo.add_job('Lower Delay Function', function_full_speed, 'Rapid Execution')

if __name__ == '__main__':
    wo.start()

```

The server will start and host a web portal on default port 8000 locally for you to view what is going on.

### Monitor

- Code below is provided in the examples/monitor_example.py file of this project.

```python
from robit import Monitor

mo = Monitor('Robit Example Monitor', key='Your-Own-Unique-Monitor-Key-That-Secure')

if __name__ == '__main__':
    mo.start()
```

The server will start and host a web portal on default port 8200 locally for you to view what is going on.

## Features

### Threaded Groups

- Execute your jobs in order and group them to have them on separate threads.

### Monitoring

- Webserver provide a super easy way to see what is going on and monitor health.

## Other Libraries Used

- Boostrap 5 (Responsive UI)
- Vue Petite (Better UX)

A robot for your bits! (Pronounced "Row-Bit")

