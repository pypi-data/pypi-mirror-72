import logging
import threading
import time

logger = logging.getLogger('concurrentevents')


def rate_limiter(limit, seconds):
    def handlerfunc(func):
        return RateLimiter(func=func, limit=limit, seconds=seconds)
    return handlerfunc


class RateLimiter:
    """
    This is an implementation of the Generic Cell Rate Algorithm which allows
    for rate limiting of function calls without the need for outside interaction

    Wikipedia: https://en.wikipedia.org/wiki/Generic_cell_rate_algorithm

    :param limit: The maximum amount of calls acceptable for the period
    :param seconds: The period at which the limit is applied to. Default 1
    :return:
    """
    def __init__(self, func, limit, seconds=1):
        if limit < 0 if isinstance(limit, int) else False:
            raise ValueError(f"rate_limiter() limit argument must be an int greater than 0, not {limit}")

        if seconds < 0 if isinstance(seconds, int) else False:
            raise ValueError(f"rate_limiter() period argument must be an int greater than 0, not {seconds}")

        self.func = func

        self.lock = threading.Lock()

        # Do setup for variables for this specific decoration
        self.last_check = time.monotonic()
        self.limit = limit
        self.seconds = seconds
        self.interval = seconds / limit

    def __call__(self, *args, **kwargs):
        t = time.monotonic()  # Represents the time of the function call

        with self.lock:
            tat = max(self.last_check, t)  # Theoretical Arrival Time

            # Check to see if that time is not within the window
            # If it's not within sleep until the window comes up
            if tat - t <= self.seconds - self.interval:
                new_tat = max(tat, t) + self.interval  # Determine the new theoretical arrival time
                self.last_check = new_tat  # Set the last_check for the next call to use
            else:
                time.sleep(self.last_check - t)

        error = None

        try:
            result = self.func(*args, **kwargs)
        except Exception as e:
            error = e
            result = None

        if error:
            raise error

        return result
