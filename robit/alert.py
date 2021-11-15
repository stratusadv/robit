class Alert:
    def __init__(
            self,
            method,
            method_kwargs: dict = {},
            health_threshold: float = 95.0,
            failed_run_threshold: int = 10,
    ):

        self.method = method
        self.method_kwargs = method_kwargs

        self.health_threshold = health_threshold
        self.failed_run_threshold = failed_run_threshold

    def check_thresholds(self, health, failed_run_count):
        message = ''

        if health <= self.health_threshold:
            message += 'Something dropped below health threshold'

        if failed_run_count >= self.failed_run_threshold:
            message += 'Something failed to run to many times'

        self.method(message, **self.method_kwargs)