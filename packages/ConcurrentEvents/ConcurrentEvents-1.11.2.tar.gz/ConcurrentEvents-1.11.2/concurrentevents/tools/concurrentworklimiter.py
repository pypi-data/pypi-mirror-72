import time
from functools import wraps


def concurrent_work_limiter(limit, timeout=0):
    """
    This decorator tool is used to limit the concurrent usage of a specific function

    Specifically any implementation keeps track of concurrent running instances of a specific function and delays
    running additional ones until the previous ones are finished

    Args:
        :param limit: A limit on how many executions of this function should happen simultaneously
        :type limit: int
    Kwargs:
        :param timeout: Timeout argument in case concurrent work takes too long
        :type timeout: int, optional

    :raises ValueError: On incorrect, limit value or timeout value
    """
    if not isinstance(limit, int):
        raise TypeError(f"concurrent_work_limiter() limit argument must be an int, not {limit}")

    if timeout < 0 if isinstance(timeout, int) else True:
        raise ValueError(f"concurrent_work_limiter() timeout argument must be an int greater than 0, not {limit}")

    def handler_function(func):
        func.working = 0
        _name = f"{func.__module__.split('.')[-1]}.{func.__name__}()"

        @wraps(func)
        def wrapper(*args, **kwargs):
            error = None

            # Delay function call till others finish
            endtime = time.monotonic() + timeout
            while func.working >= limit:
                if timeout > 0:
                    if endtime - time.monotonic() <= 0.0:
                        raise TimeoutError(f"ConcurrentWorkLimiter({_name}) timeout({timeout}s)")
                time.sleep(0.25)

            func.working += 1

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                error = e
                result = None

            func.working -= 1

            if error:
                raise error

            return result
        return wrapper
    return handler_function
