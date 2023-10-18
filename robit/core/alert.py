import logging
from datetime import timedelta
from typing import Callable

from robit.core.clock import Clock
from robit.core.health import Health


class Alert:
    def __init__(
            self,
            method: Callable,
            method_kwargs: dict = None,
            health_threshold: float = 95.0,
            hours_between_messages: int = 24,
    ) -> None:

        self.method = method
        self.clock = Clock()

        if method_kwargs is not None:
            self.method_kwargs = method_kwargs
        else:
            self.method_kwargs = dict()

        self.health_threshold = health_threshold
        self.hours_between_messages = hours_between_messages

        self.last_message_datetime = self.clock.now_tz - timedelta(hours=self.hours_between_messages)

    def check_health_threshold(self, name: str, health: Health) -> None:
        if self.clock.now_tz >= self.last_message_datetime + timedelta(hours=self.hours_between_messages):
            if health.percentage_hundreds <= self.health_threshold:
                alert_message = f'ALERT: {name} dropped below the {self.health_threshold} percentage health threshold.'
                self.method_kwargs['alert_message'] = alert_message

                try:
                    self.method(**self.method_kwargs)
                    self.last_message_datetime = self.clock.now_tz
                    logging.warning(alert_message)
                except Exception as e:
                    failed_message = f'FAILURE: Alert method failed on exception "{e}"'
                    logging.error(failed_message)
