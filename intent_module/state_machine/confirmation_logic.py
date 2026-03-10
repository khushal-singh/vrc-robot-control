import time


class ConfirmationManager:

    def __init__(self, timeout=5):
        self.timeout = timeout
        self.start_time = None

    def start_timer(self):
        self.start_time = time.time()

    def is_timeout(self):
        if self.start_time is None:
            return False
        return (time.time() - self.start_time) > self.timeout