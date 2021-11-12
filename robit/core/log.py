from robit.core.clock import Clock


class Log:
    def __init__(
            self,
            max_messages: int = 5,
            utc_offset: int = 0,
    ):
        self.max_messages = max_messages
        self.message_list = list()

        self.clock = Clock(utc_offset=utc_offset)

    def add_message(self, message: str):
        self.message_list.insert(0, f'[{self.clock.now_tz_verbose}] {message}')
        self.trim()

    def trim(self):
        if len(self.message_list) > self.max_messages:
            del self.message_list[self.max_messages:]

    def as_dict(self):
        return {
            'log': self.message_list
        }
