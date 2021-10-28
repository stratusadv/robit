# Robit

Lightweight (no installed dependencies) Service Worker Framework

## Usage

```python
from robit import Worker

from time import sleep

wo = Worker('Test Worker')

def test_function():
    sleep(10)

wo.add_job('Test Function', test_function)

if __name__ == '__main__':
    wo.run()
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

A robot for your bits! (Pronounced "Row-Bit")

