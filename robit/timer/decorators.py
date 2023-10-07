from typing import Callable


def timing_decorator(func) -> Callable:
    def wrapper(self, *args, **kwargs) -> Callable:
        if hasattr(self, 'timer'):
            self.timer.start()
            result = func(self, *args, **kwargs)
            self.timer.stop()
        else:
            result = func(self, *args, **kwargs)
        return result
    return wrapper
