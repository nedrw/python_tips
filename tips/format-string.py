from tips import finfo


@finfo
def base_fstring():
    """
    Base function to demonstrate f-strings in Python.

    :returns: This function does not return any value.
    """
    x = 3
    y = 4
    print(f"x: {x}, y: {y}")


@finfo
def expression_fstring():
    """
    Prints expression in an f-string.

    :returns: None
    """
    x = 3
    y = 4
    print(f"{x=}, {y=}, {x > y = }")


@finfo
def nested_fstring():
    """
    Generates and prints a formatted string using nested f-strings in Python.

    :returns: This function does not return any value.
    """
    x = 3
    y = 4
    print(f"{f'{x=}'}, {y=}")


@finfo
def number_fstring():
    """
    A function that demonstrates the usage of f-strings for formatting
    numbers in Python. It prints out a large integer and a floating-point
    number, each formatted in different ways to show various f-string
    capabilities.

    :returns: This function does not return any value.
    """
    x = 3000000
    y = 44.44444
    print(f"{x=:_}, {x=:,}, {x=:_.1f}")
    print(f"{y=:.2f}, {y=:.1f}")


@finfo
def datetime_fstring():
    """
    Demonstrates the usage of f-strings with datetime objects to format and print
    the current date and time in different formats.

    :returns: None
    """
    from datetime import datetime

    x = datetime.now()
    print(f"{x:%x}")
    print(f"{x:%c}")
    print(f"{x:%y-%m-%d %H:%M:%S}")


@finfo
def align_fstring():
    """
    Demonstrates various string alignment and formatting techniques using f-strings in Python.
    The function showcases how to center, left-justify, and right-justify strings with or without
    fill characters, providing a visual representation of the different formatting options available.

    :returns: None. This function is used for demonstration purposes and does not return any value.
    """
    x = "words"
    y = 20
    print(f"{x:^20}...")
    print(f"{x:^{y}}...")
    print(f"{x:=^{y}}...")
    print(f"{x:=<{y}}...")
    print(f"{x:=>{y}}...")


@finfo
def struct_fstring():
    """
    Demonstrates the usage of custom __format__ method in a class to control
    how instances are formatted with f-strings. The Word class is defined with
    an x and y attribute, and its __format__ method is overridden to handle
    different format specifications, allowing for flexible formatting based on
    the provided format spec.

    :returns: None
    """
    class Word:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __format__(self, format_spec):
            match format_spec:
                case "1":
                    return f"{self.x}"
                case "2":
                    return f"{self.y}"
            return f"{self.x=}, {self.y=}"

    print(f"{Word(1, 2)=}")  # __repr__
    print(f"{Word(1, 2)}")
    print(f"{Word(1, 2)=:1}")
    print(f"{Word(1, 2)=:2}")


def examples():
    """
    A collection of functions demonstrating various uses of f-strings in Python.

    Functions:
        - base_fstring: Demonstrates the basic usage of f-strings for string formatting.
        - expression_fstring: Shows how to use expressions within f-strings.
        - nested_fstring: Illustrates the use of nested f-strings.
        - number_fstring: Demonstrates formatting numbers with f-strings.
        - datetime_fstring: Illustrates formatting dates and times using f-strings.
        - align_fstring: Shows how to align text using f-strings.
        - struct_fstring: Demonstrates the use of structured data with f-strings.

    .. note::
       This module is intended for educational purposes, showcasing the versatility
       of f-strings in different scenarios.
    """
    base_fstring()
    expression_fstring()
    nested_fstring()
    number_fstring()
    datetime_fstring()
    align_fstring()
    struct_fstring()
