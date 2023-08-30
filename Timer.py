import time


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        self._start_time = time.perf_counter()

    def elapsed(self, expected_time):
        if self._start_time is None:
            return None
        elapsed_time = time.perf_counter() - self._start_time
        if expected_time > elapsed_time:
            return False
        else:
            return True
