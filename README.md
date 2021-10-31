# Robit

- Lightweight (no installed dependencies) Service Worker Framework

## Usage

- Code below is provided in the demo.py file of this project.

```python
from robit import Worker
from time import sleep
import random

wo = Worker('Robit Example Worker')

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

The server will start and host a web portal on port 8000 locally for you to view what is going on.

## Features

### Threaded Groups

- Execute your jobs in order and group them to have them on separate threads.

### Monitoring

- Webserver provide a super easy way to see what is going on and monitor health.

## Other Libraries Used

- Boostrap 5 (Responsive UI)
- Vue Petite (Better UX)

A robot for your bits! (Pronounced "Row-Bit")

