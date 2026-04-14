from tips import finfo


def example_basic_generator():
    """基本的生成器函数"""
    print("\n=== 基本生成器 ===")

    def count_up_to(n):
        """一个简单的生成器函数，生成从0到n-1的数字"""
        i = 0
        while i < n:
            yield i
            i += 1

    # 创建生成器对象
    gen = count_up_to(5)
    print(f"生成器对象: {gen}")
    print(f"生成器类型: {type(gen)}")

    # 逐个获取值
    print("逐个获取值:", end=" ")
    for num in gen:
        print(num, end=" ")
    print()

    # 生成器只能迭代一次
    gen2 = count_up_to(3)
    print("转列表:", list(gen2))
    print("再次转列表:", list(gen2))  # 空，因为生成器已经耗尽


def example_generator_expression():
    """生成器表达式"""
    print("\n=== 生成器表达式 ===")

    # 列表推导式（立即计算，占用内存）
    squares_list = [x**2 for x in range(10)]
    print(f"列表推导式: {squares_list}")

    # 生成器表达式（惰性计算，节省内存）
    squares_gen = (x**2 for x in range(10))
    print(f"生成器表达式: {squares_gen}")
    print(f"转为列表: {list(squares_gen)}")

    # 内存对比：大序列
    import sys

    big_list = [x for x in range(10000)]
    big_gen = (x for x in range(10000))

    print(f"\n列表占用内存: {sys.getsizeof(big_list)} bytes")
    print(f"生成器占用内存: {sys.getsizeof(big_gen)} bytes")


def example_lazy_evaluation():
    """惰性求值和内存优化"""
    print("\n=== 惰性求值 ===")

    def fibonacci_generator(n):
        """生成斐波那契数列的生成器"""
        a, b = 0, 1
        count = 0
        while count < n:
            yield a
            a, b = b, a + b
            count += 1

    # 只在需要时才计算下一个值
    fib_gen = fibonacci_generator(10)
    print("斐波那契数列:", list(fib_gen))

    # 处理大文件示例（模拟）
    def read_large_file(lines=1000):
        """模拟读取大文件，每次只加载一行到内存"""
        for i in range(lines):
            yield f"Line {i}: Some data..."

    # 使用生成器处理，内存中只有当前行
    file_gen = read_large_file(5)
    print("\n模拟读取大文件:")
    for line in file_gen:
        print(f"  处理: {line}")


def example_infinite_sequence():
    """无限序列"""
    print("\n=== 无限序列 ===")

    def infinite_counter():
        """无限计数器"""
        n = 0
        while True:
            yield n
            n += 1

    def infinite_cycle(iterable):
        """无限循环迭代"""
        while True:
            for item in iterable:
                yield item

    # 无限计数器（配合takewhile或islice使用）
    from itertools import islice

    counter = infinite_counter()
    print("无限计数器前10个:", list(islice(counter, 10)))

    # 无限循环
    cycler = infinite_cycle(["A", "B", "C"])
    print("无限循环前8个:", list(islice(cycler, 8)))

    # 实际应用：生成唯一ID
    def generate_ids(prefix):
        """生成唯一ID的生成器"""
        n = 1
        while True:
            yield f"{prefix}_{n:04d}"
            n += 1

    id_gen = generate_ids("USER")
    print("\n生成唯一ID:")
    for _ in range(5):
        print(f"  {next(id_gen)}")


def example_pipeline_pattern():
    """管道模式：链式处理数据"""
    print("\n=== 管道模式 ===")

    def read_data():
        """模拟数据源"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for item in data:
            yield item

    def filter_even(gen):
        """过滤偶数"""
        for item in gen:
            if item % 2 == 0:
                yield item

    def square_numbers(gen):
        """平方运算"""
        for item in gen:
            yield item**2

    def limit_results(gen, n):
        """限制结果数量"""
        count = 0
        for item in gen:
            if count >= n:
                break
            yield item
            count += 1

    # 构建管道
    pipeline = limit_results(square_numbers(filter_even(read_data())), 3)
    print("管道处理结果:", list(pipeline))

    # 更复杂的管道：处理文本
    def text_lines():
        """文本数据源"""
        texts = [
            "Hello World",
            "Python is great",
            "Generators are powerful",
            "Lazy evaluation saves memory",
        ]
        for text in texts:
            yield text

    def to_lowercase(gen):
        """转为小写"""
        for text in gen:
            yield text.lower()

    def filter_long(gen, min_length):
        """过滤长文本"""
        for text in gen:
            if len(text) > min_length:
                yield text

    def extract_words(gen):
        """提取单词"""
        for text in gen:
            for word in text.split():
                yield word

    # 构建文本处理管道
    text_pipeline = extract_words(filter_long(to_lowercase(text_lines()), 10))
    print("\n文本处理管道:", list(text_pipeline))


def example_yield_from():
    """yield from 语法"""
    print("\n=== yield from ===")

    def sub_generator():
        """子生成器"""
        yield 1
        yield 2
        yield 3

    def main_generator():
        """主生成器使用yield from委托给子生成器"""
        yield "Start"
        yield from sub_generator()
        yield from [4, 5]
        yield "End"

    print("yield from结果:", list(main_generator()))

    # 实际应用：扁平化嵌套结构
    def flatten(nested):
        """递归展平嵌套列表"""
        for item in nested:
            if isinstance(item, list):
                yield from flatten(item)
            else:
                yield item

    nested_list = [1, [2, 3], [4, [5, 6, [7, 8]]], 9]
    print("扁平化嵌套列表:", list(flatten(nested_list)))

    # 文件系统遍历示例
    def traverse_tree(tree):
        """遍历树形结构"""
        if isinstance(tree, dict):
            for key, value in tree.items():
                yield key
                yield from traverse_tree(value)
        elif isinstance(tree, list):
            for item in tree:
                yield from traverse_tree(item)
        else:
            yield tree

    file_tree = {
        "root": [
            {"folder1": ["file1.txt", "file2.txt"]},
            {"folder2": ["file3.txt"]},
        ]
    }
    print("树形结构遍历:", list(traverse_tree(file_tree)))


def example_generator_state():
    """生成器的状态管理"""
    print("\n=== 生成器状态 ===")

    def stateful_generator():
        """演示生成器的不同状态"""
        print("  状态: GEN_CREATED (创建后，未启动)")
        yield 1
        print("  状态: GEN_SUSPENDED (在yield处暂停)")
        yield 2
        print("  状态: GEN_SUSPENDED (在yield处暂停)")
        yield 3
        print("  状态: GEN_CLOSED (生成器结束)")

    from inspect import getgeneratorstate

    gen = stateful_generator()
    print(f"初始状态: {getgeneratorstate(gen)}")

    print(f"\n第一次next(): {next(gen)}")
    print(f"当前状态: {getgeneratorstate(gen)}")

    print(f"\n第二次next(): {next(gen)}")
    print(f"当前状态: {getgeneratorstate(gen)}")

    print(f"\n第三次next(): {next(gen)}")
    print(f"当前状态: {getgeneratorstate(gen)}")

    # 生成器结束
    try:
        next(gen)
    except StopIteration:
        print("生成器已结束")
        print(f"最终状态: {getgeneratorstate(gen)}")


def example_send_method():
    """生成器的send方法：协程基础"""
    print("\n=== send方法与双向通信 ===")

    def accumulator():
        """可接收外部值的累加器"""
        total = 0
        while True:
            # yield接收外部send发送的值
            received = yield total
            if received is None:
                break
            total += received
            print(f"  接收: {received}, 当前总和: {total}")

    # 创建生成器
    acc = accumulator()

    # 必须先启动生成器（或使用next）
    initial_value = next(acc)
    print(f"初始值: {initial_value}")

    # 发送值并接收结果
    result = acc.send(10)
    print(f"发送10后: {result}")

    result = acc.send(20)
    print(f"发送20后: {result}")

    result = acc.send(30)
    print(f"发送30后: {result}")

    # 关闭生成器
    acc.close()
    print("生成器已关闭")


def example_throw_close():
    """生成器的异常处理和关闭"""
    print("\n=== throw和close方法 ===")

    def error_handling_generator():
        """处理异常的生成器"""
        try:
            yield 1
            yield 2
            yield 3
        except ValueError as e:
            print(f"  生成器捕获异常: {e}")
            yield "error"
        finally:
            print("  生成器清理资源")

    gen = error_handling_generator()
    print(f"第一个值: {next(gen)}")

    # 向生成器抛出异常
    result = gen.throw(ValueError, "Something went wrong")
    print(f"异常后的值: {result}")

    # 继续执行
    try:
        next(gen)
    except StopIteration:
        print("生成器正常结束")

    # close方法演示
    print("\nclose方法:")

    def closeable_gen():
        try:
            yield 1
            yield 2
            yield 3
        finally:
            print("  执行清理代码")

    gen2 = closeable_gen()
    print(f"第一个值: {next(gen2)}")
    gen2.close()
    print("生成器已关闭")

    try:
        next(gen2)
    except StopIteration:
        print("尝试访问已关闭的生成器: StopIteration")


def example_generator_tools():
    """生成器相关工具函数"""
    print("\n=== 生成器工具函数 ===")

    # enumerate with generator
    def enum_gen():
        yield "apple"
        yield "banana"
        yield "cherry"

    print("enumerate:")
    for idx, value in enumerate(enum_gen()):
        print(f"  {idx}: {value}")

    # zip with generators
    gen1 = (x for x in range(3))
    gen2 = (chr(65 + x) for x in range(3))
    print("\nzip:")
    for num, letter in zip(gen1, gen2):
        print(f"  {num} -> {letter}")

    # any/all with generators
    def check_values():
        yield 0
        yield 1
        yield 2

    print(f"\nany: {any(check_values())}")
    print(f"all: {all(check_values())}")

    # sorted with generator
    def random_gen():
        yield 3
        yield 1
        yield 4
        yield 1
        yield 5

    print(f"\nsorted: {sorted(random_gen())}")

    # sum/min/max with generator
    numbers = (x for x in range(1, 6))
    print(f"sum: {sum(numbers)}")


@finfo(
    description="演示生成器与yield机制：惰性求值、内存优化、无限序列、管道模式、yield from、协程基础",
    tags=["generator", "yield", "lazy-evaluation", "coroutine"],
    difficulty="intermediate",
)
def main():
    example_basic_generator()
    example_generator_expression()
    example_lazy_evaluation()
    example_infinite_sequence()
    example_pipeline_pattern()
    example_yield_from()
    example_generator_state()
    example_send_method()
    example_throw_close()
    example_generator_tools()


if __name__ == "__main__":
    main()
