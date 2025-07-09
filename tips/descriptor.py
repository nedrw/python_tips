from tips import finfo


class TypedProperty:
    def __init__(self, name, dtype):
        self.name = name
        self.dtype = dtype

    def __get__(self, instance, owner):
        if instance is None:
            return self
        print(f"Getting {self.name}")
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.dtype):
            raise TypeError(f"Expected {self.dtype}, got {type(value)}")
        print(f"Setting {self.name} to {value}")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        print(f"Deleting {self.name}")
        del instance.__dict__[self.name]


# 使用描述符
class Person:
    name = TypedProperty("name", str)
    age = TypedProperty("age", int)

    def __init__(self, name, age):
        self.name = name
        self.age = age


# 描述符机制用于控制属性访问行为。一个类如果定义了 __get__、__set__ 或 __delete__ 中的至少一个方法，就被认为是一个描述符。
# 描述符通常用于实现属性（property）的自定义行为，比如 getter、setter 或 deleter。
@finfo
def main():
    p = Person("Alice", 30)
    print(p.name)  # 输出: Alice
    print(p.age)  # 输出: 30

    p.age = 31
    del p.name


if __name__ == "__main__":
    main()
