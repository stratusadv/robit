import logging
from datetime import datetime, timedelta
from typing import Callable

from robit.core.health import Health


class Alert:
    def __init__(
            self,
            method: Callable,
            method_kwargs: dict = None,
            health_threshold: float = 95.0,
            hours_between_messages: int = 24,
    ):

        self.method = method

        if method_kwargs is not None:
            self.method_kwargs = method_kwargs
        else:
            self.method_kwargs = dict()

        self.health_threshold = health_threshold
        self.hours_between_messages = hours_between_messages

        self.last_message_datetime = datetime.now() - timedelta(hours=self.hours_between_messages)

    def check_health_threshold(self, name, health: Health):
        if datetime.now() >= self.last_message_datetime + timedelta(hours=self.hours_between_messages):
            if health.percentage_hundreds <= self.health_threshold:
                alert_message = f'ALERT: {name} dropped below the {self.health_threshold} percentage health threshold.'
                self.method_kwargs['alert_message'] = alert_message

                try:
                    self.method(**self.method_kwargs)
                    self.last_message_datetime = datetime.now()
                    logging.warning(alert_message)
                except Exception as e:
                    failed_message = f'ERROR: Alert method failed on exception "{e}"'
                    logging.warning(failed_message)
