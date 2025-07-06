import functools


def finfo(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        print(f"\n>>>{func.__module__}:{func.__name__}")
        return func(*args, **kwargs)
    return inner
