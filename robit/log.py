class Log:
    def __init__(self, max_entries: int = 5):
        self.max_entries = max_entries
        self.message_list = list()

    def add_message(self, message: str):
        self.message_list.insert(0, message)

    def as_dict(self):
        return {
            'log': self.message_list
        }
