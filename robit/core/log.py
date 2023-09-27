from collections import deque

from robit.core.clock import Clock


class Log:

    def __init__(
            self,
            max_messages: int = 5,
    ) -> None:
        # deque are optimized for appending and popping from both ends.
        self.messages: deque = deque(maxlen=max_messages)

        self.clock = Clock()

    def add_message(self, message: str) -> None:
        self.messages.appendleft(f'[{self.clock.now_tz_verbose}] {message}')

    def as_dict(self) -> dict:
        # Need to convert deque to list to be able to serialize to JSON.
        return {
            'log': list(self.messages)
        }
