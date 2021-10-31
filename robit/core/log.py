class Log:
    def __init__(self, max_messages: int = 5):
        self.max_messages = max_messages
        self.message_list = list()

    def add_message(self, message: str):
        self.message_list.insert(0, message)
        self.trim()

    def trim(self):
        if len(self.message_list) > self.max_messages:
            del self.message_list[self.max_messages:]

    def as_dict(self):
        return {
            'log': self.message_list
        }
