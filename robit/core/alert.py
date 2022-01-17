import logging
from datetime import datetime, timedelta

from robit.core.health import Health


class Alert:
    def __init__(
            self,
            **kwargs,
    ):

        if 'alert_method' in kwargs:
            self.method = kwargs['alert_method']

        if 'alert_method_kwargs' in kwargs:
            self.method_kwargs = kwargs['alert_method_kwargs']
        else:
            self.method_kwargs = dict()

        if 'alert_health_threshold' in kwargs:
            self.health_threshold = kwargs['alert_health_threshold']
        else:
            self.health_threshold = 95.0

        if 'alert_hours_between_messages' in kwargs:
            self.hours_between_messages = kwargs['alert_hours_between_messages']
        else:
            self.hours_between_messages = 24

        self.last_message_datetime = datetime.now() - timedelta(hours=self.hours_between_messages)

    def check_health_threshold(self, name, health: Health):
        if datetime.now() >= self.last_message_datetime + timedelta(hours=self.hours_between_messages):
            if health.percentage_hundreds <= self.health_threshold:
                alert_message = f'{name} dropped below the {self.health_threshold} health threshold.'
                self.method_kwargs['alert_message'] = alert_message
                try:
                    self.method(**self.method_kwargs)
                    self.last_message_datetime = datetime.now()
                except Exception as e:
                    failed_message = f'Failed on Exception: {e}'
                    logging.warning(failed_message)
