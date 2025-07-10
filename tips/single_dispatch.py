from functools import singledispatch, singledispatchmethod

from tips import finfo


# 主函数定义，处理默认情况（例如 int 类型）
@singledispatch
def process_data(data):
    print(f"Processing default data: {data}")


# 为 str 类型注册一个特定实现
@process_data.register(str)
def _(data):
    print(f"Processing string data: {data}")


# 为 float 类型注册一个特定实现
@process_data.register(float)
def _(data):
    print(f"Processing float data: {data}")


class DataProcessor:
    @singledispatchmethod
    def process_data(self, data):
        print(f"Processing default data: {data}")

    @process_data.register(str)
    def _(self, data):
        print(f"Processing string data: {data}")

    @process_data.register(float)
    def _(self, data):
        print(f"Processing float data: {data}")


@finfo
def main():
    process_data(10)  # 调用默认实现
    process_data("hello")  # 调用 str 实现
    process_data(3.14)  # 调用 float 实现

    processor = DataProcessor()
    processor.process_data(10)  # 默认实现
    processor.process_data("hello")  # str 实现
    processor.process_data(3.14)  # float 实现


if __name__ == "__main__":
    main()
