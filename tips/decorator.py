from functools import wraps

from tips import finfo


def simple_decorator(func):
    # 简单装饰器
    def wrapper():
        print("Before function call")
        func()
        print("After function call")

    return wrapper


@simple_decorator
def say_hello():
    print("Hello")


def decorator_with_args(func):
    # 支持带参数方法的装饰器
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)

    return wrapper


@decorator_with_args
def greet(name, message="Hi"):
    print(f"{message}, {name}")


def repeat(num_times):
    # 带参数的装饰器
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


@repeat(3)
def say_hi():
    print("Hi!")


def bold(func):
    def wrapper():
        return f"<b>{func()}</b>"

    return wrapper


def italic(func):
    def wrapper():
        return f"<i>{func()}</i>"

    return wrapper


@bold
@italic
def get_text():
    # 组合装饰器
    return "Hello, world!"


def my_decorator(func):
    # functools.wraps 保留函数信息
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Logging before call")
        return func(*args, **kwargs)

    return wrapper


@my_decorator
def example():
    """An example docstring."""
    print("In example")


class CountCalls:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__}")
        return self.func(*args, **kwargs)


@CountCalls
def say_welcome():
    # 类装饰器
    print("Welcome")


# 装饰器的本质是在方法外层进行额外包装
# @decorator
# func(*args, **kwargs)
# 实质上等价于表达式
# func = decorator(func)


@finfo
def main():
    say_hello()

    greet("Alice", message="Hello")

    say_hi()

    print(get_text())

    print(example.__doc__)
    print(example.__name__)

    say_welcome()
    say_welcome()


if __name__ == "__main__":
    main()
