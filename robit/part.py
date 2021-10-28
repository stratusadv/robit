import logging


class Part:
    def __init__(self, name, method):
        self.name = name
        self.method = method
        self.status = False

    def run(self):
        logging.warning(f'Starting: Part "{self.name}"')
        try:
            self.method()
            logging.warning(f'Success: Part "{self.name}" executed')
            self.status = True
        except Exception as e:
            logging.warning(f'Failed: Part "{self.name}" on Exception: {e}')
            self.status = False

    def as_dict(self):
        return {
            'name': self.name,
            'method': self.method.__name__,
            'status': self.status,
        }