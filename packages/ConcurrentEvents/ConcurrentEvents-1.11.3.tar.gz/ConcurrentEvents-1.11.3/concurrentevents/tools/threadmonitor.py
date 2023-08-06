from functools import wraps

_monitoring = {}


def thread_monitor(func):
    """
    A decorator to bse used in monitoring functions that have any possibility of causing a deadlock

    Default implementation is under ConcurrentWorkLimiter and ResourceManager as both have
    functionality where threads can interact indirectly

    Debug can be used through this by simply printing the dictionary and it will display how many of each
    monitored function is running at any point in time

    Args:
        :param func: a function which will be added to the monitoring dict
        :type func: class:`function`
    """

    _name = f"{func.__module__.split('.')[-1]}.{func.__name__}()"
    _monitoring.update({_name: 0})

    @wraps(func)
    def wrapper(*args, **kwargs):
        error = None

        _monitoring[_name] += 1

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            error = e
            result = None

        _monitoring[_name] -= 1

        if error:
            raise error

        return result
    return wrapper
