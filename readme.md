# Robit - Service Worker Framework

A robot for your bits! (Pronounced "Row-Bit")

## Usage

```python
from robit import Robit

from time import sleep

rb = Robit('Mr Wiggles')

def test_function():
    sleep(10)

rb.add_part('Test Function', test_function)

if __name__ == '__main__':
    rb.run()
```

The server will start and host a web portal on port 8000 locally for you to view what is going on.

## Features

### Monitoring

- Webserver

### Logging

- File Based
- Webserver

### Management

- Webserver

## Other Libraries Used

- Boostrap 5
- Vue Petite

