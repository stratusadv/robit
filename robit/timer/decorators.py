def timing_decorator(func):
    def wrapper(self, *args, **kwargs):
        if hasattr(self, 'timer'):
            self.timer.start()
            result = func(self, *args, **kwargs)
            self.timer.stop()
        else:
            result = func(self, *args, **kwargs)
        return result
    return wrapper
