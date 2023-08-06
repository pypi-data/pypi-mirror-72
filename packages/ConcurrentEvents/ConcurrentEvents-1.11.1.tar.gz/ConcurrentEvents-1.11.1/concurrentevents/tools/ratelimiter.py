import time
from functools import wraps


def rate_limiter(limit, period=1):
    """
    This is an implementation of the Generic Cell Rate Algorithm which allows
    for rate limiting of function calls without the need for outside interaction

    Wikipedia: https://en.wikipedia.org/wiki/Generic_cell_rate_algorithm

    :param limit: The maximum amount of calls acceptable for the period
    :param period: The period at which the limit is applied to. Default 1
    :return:
    """

    if limit < 0 if isinstance(limit, int) else False:
        raise ValueError(f"rate_limiter() limit argument must be an int greater than 0, not {limit}")

    if period < 0 if isinstance(period, int) else False:
        raise ValueError(f"rate_limiter() period argument must be an int greater than 0, not {period}")

    # Do setup for variables for this specific decoration
    last_check = time.monotonic()
    interval = period / limit
    tat = 0

    def handlerfunction(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # Represents the time of the call
            t = time.monotonic()

            # Theoretical Arrival Time
            # Find the maximum point either tat or now
            tat = max(last_check, t)

            # Check to see if that time is not within the window
            # If it's not within sleep until the window comes up
            if tat - t <= (period - interval):
                # Determine the new theoretical arrival time
                new_tat = max(tat, t) + interval
                # Set that tat for the next call to use
                tat = new_tat
                # Sleep for the remaining time needed to finish this window
                time.sleep(new_tat - t)

            error = None

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                error = e
                result = None

            if error:
                raise error

            return result
        return wrapper
    return handlerfunction
