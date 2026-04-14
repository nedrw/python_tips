"""
海象运算符（Walrus Operator）- Python 3.8引入的赋值表达式

海象运算符（:=）允许在表达式内部进行赋值操作，避免了重复计算和冗余代码。

核心特性：
- 语法：variable := expression
- 在表达式内部赋值并返回值
- 减少重复计算，提高代码可读性
- 适用于循环、条件判断、推导式等场景
"""

from tips import finfo

# ============================================================================
# 辅助类和函数（模块级别）
# ============================================================================


def get_expensive_value():
    """模拟一个计算成本较高的函数"""
    print("    [计算值...]", end=" ")
    return 42


def process(x):
    """模拟一个处理函数"""
    return x * x


class MockFile:
    """模拟文件的readline行为"""

    def __init__(self, lines):
        self.lines = lines
        self.index = 0

    def readline(self):
        if self.index < len(self.lines):
            line = self.lines[self.index]
            self.index += 1
            return line
        return ""


def get_batch(data, batch_size=3):
    """获取一批数据"""
    return data[:batch_size]


def expensive_computation(x):
    """模拟昂贵的计算"""
    return x * x * x


# ============================================================================
# 示例函数
# ============================================================================


def example_basic_syntax():
    """示例1-2：海象运算符基础语法"""
    print("=" * 60)
    print("1. 海象运算符基础")
    print("=" * 60)

    # 示例1：基本语法
    # 传统写法
    text = "Hello, World!"
    length = len(text)
    if length > 10:
        print(f"  传统写法: 文本长度 {length} 大于10")

    # 海象运算符写法
    if (n := len(text)) > 10:
        print(f"  海象运算符: 文本长度 {n} 大于10")

    # 示例2：避免重复计算
    print("\n  避免重复计算:")
    data = [1, 2, 3, 4, 5]

    # 传统写法：调用两次len()
    if len(data) > 3:
        print(f"    传统写法: 列表长度 {len(data)} 大于3")  # 重复调用

    # 海象运算符：只调用一次
    if (count := len(data)) > 3:
        print(f"    海象运算符: 列表长度 {count} 大于3")  # 重用变量


def example_while_loop():
    """示例3-4：在while循环中使用"""
    print("\n" + "=" * 60)
    print("2. 在while循环中使用")
    print("=" * 60)

    # 示例3：读取文件直到结束
    print("  模拟文件读取:")
    lines = ["第一行", "第二行", "第三行", "第四行", "第五行"]
    index = 0

    # 传统写法
    print("\n  传统写法（需要初始化变量）:")
    line = lines[index] if index < len(lines) else None
    while line is not None:
        print(f"    {line}")
        index += 1
        line = lines[index] if index < len(lines) else None

    # 重置索引
    index = 0

    # 海象运算符写法（更简洁）
    print("\n  海象运算符写法（更简洁）:")
    while index < len(lines) and (line := lines[index]):
        print(f"    {line}")
        index += 1

    # 示例4：处理用户输入
    print("\n  模拟用户输入处理:")
    inputs = ["hello", "world", "quit", "ignored"]

    # 传统写法
    print("\n  传统写法:")
    idx = 0
    user_input = inputs[idx]
    while user_input != "quit":
        print(f"    处理: {user_input}")
        idx += 1
        if idx < len(inputs):
            user_input = inputs[idx]
        else:
            break

    # 海象运算符写法
    print("\n  海象运算符写法:")
    idx = 0
    while idx < len(inputs) and (user_input := inputs[idx]) != "quit":
        print(f"    处理: {user_input}")
        idx += 1


def example_if_statement():
    """示例5-6：在if语句中使用"""
    print("\n" + "=" * 60)
    print("3. 在if语句中使用")
    print("=" * 60)

    # 示例5：条件判断中的赋值
    print("  条件判断中使用:")
    # 传统写法：需要先调用函数
    value = get_expensive_value()
    print(f"→ {value}")
    if value > 40:
        print(f"    传统写法: 值 {value} 大于40")

    # 海象运算符：在条件中直接赋值
    if (val := get_expensive_value()) > 40:
        print(f"    海象运算符: 值 {val} 大于40")

    # 示例6：嵌套条件判断
    print("\n  嵌套条件判断:")
    config = {"threshold": 50, "enabled": True}

    # 传统写法
    if "threshold" in config:
        threshold = config["threshold"]
        if threshold > 30:
            print(f"    传统写法: 阈值 {threshold} 大于30")

    # 海象运算符
    if (threshold := config.get("threshold")) and threshold > 30:
        print(f"    海象运算符: 阈值 {threshold} 大于30")


def example_list_comprehension():
    """示例7-8：在列表推导式中使用"""
    print("\n" + "=" * 60)
    print("4. 在列表推导式中使用")
    print("=" * 60)

    # 示例7：过滤并转换
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"  原始列表: {numbers}")

    # 传统写法：需要两次调用函数
    # 传统写法
    result1 = [process(x) for x in numbers if process(x) > 25]
    print(f"  传统写法（重复计算）: {result1}")

    # 海象运算符：避免重复计算
    result2 = [y for x in numbers if (y := process(x)) > 25]
    print(f"  海象运算符（避免重复）: {result2}")

    # 示例8：复杂数据处理
    data_items = [
        {"name": "Alice", "score": 85},
        {"name": "Bob", "score": 92},
        {"name": "Charlie", "score": 78},
        {"name": "David", "score": 95},
    ]

    print(f"\n  学生数据: {[item['name'] for item in data_items]}")

    # 传统写法：需要多次访问字典
    high_scorers = []
    for item in data_items:
        score = item.get("score")
        if score and score > 80:
            high_scorers.append((item["name"], score))

    print(f"  传统写法: 高分学生 {high_scorers}")

    # 海象运算符：更简洁
    high_scorers2 = [
        (item["name"], score)
        for item in data_items
        if (score := item.get("score")) and score > 80
    ]
    print(f"  海象运算符: 高分学生 {high_scorers2}")


def example_dict_set_comprehension():
    """示例9-10：在字典和集合推导式中使用"""
    print("\n" + "=" * 60)
    print("5. 在字典和集合推导式中使用")
    print("=" * 60)

    # 示例9：字典推导式
    words = ["hello", "world", "python", "programming", "code"]
    print(f"  单词列表: {words}")

    # 传统写法
    word_lengths1 = {}
    for word in words:
        length = len(word)
        if length > 5:
            word_lengths1[word] = length

    print(f"  传统写法: {word_lengths1}")

    # 海象运算符
    word_lengths2 = {word: length for word in words if (length := len(word)) > 5}
    print(f"  海象运算符: {word_lengths2}")

    # 示例10：集合推导式
    numbers2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"\n  数字列表: {numbers2}")

    # 海象运算符
    squares = {sq for x in numbers2 if (sq := x * x) > 25}
    print(f"  大于25的平方数: {squares}")


def example_function_call():
    """示例11-12：在函数调用中使用"""
    print("\n" + "=" * 60)
    print("6. 在函数调用中使用")
    print("=" * 60)

    # 示例11：函数参数中的赋值
    def process_data(data, threshold=10):
        """处理数据的函数"""
        return f"处理 {len(data)} 个数据项，阈值 {threshold}"

    raw_data = [1, 2, 3, 4, 5, 6, 7, 8]

    # 传统写法
    data_copy = raw_data.copy()
    result = process_data(data_copy, threshold=5)
    print(f"  传统写法: {result}")

    # 海象运算符
    result = process_data(data := raw_data.copy(), threshold=5)
    print(f"  海象运算符: {result}")
    print(f"  data变量仍可用: {data[:3]}...")

    # 示例12：避免重复调用昂贵函数
    import re

    text_to_match = "Hello, Python 3.11!"

    # 传统写法：需要两次匹配
    print(f"\n  文本: '{text_to_match}'")
    pattern = r"Python (\d+\.\d+)"
    match = re.search(pattern, text_to_match)
    if match:
        print(f"  传统写法: 找到Python版本 {match.group(1)}")

    # 海象运算符：更简洁
    if match := re.search(pattern, text_to_match):
        print(f"  海象运算符: 找到Python版本 {match.group(1)}")


def example_real_world_usage():
    """示例13-16：实际应用场景"""
    print("\n" + "=" * 60)
    print("7. 实际应用场景")
    print("=" * 60)

    # 示例13：读取文件内容
    print("  模拟文件读取（传统 vs 海象运算符）:")

    mock_file = MockFile(["line 1\n", "line 2\n", "line 3\n", ""])

    # 传统写法
    print("    传统写法:")
    mock_file.index = 0  # 重置
    line = mock_file.readline()
    while line:
        print(f"      {line.strip()}")
        line = mock_file.readline()

    # 海象运算符写法
    print("    海象运算符:")
    mock_file.index = 0  # 重置
    while line := mock_file.readline():
        print(f"      {line.strip()}")

    # 示例14：批量数据处理
    print("\n  批量数据处理:")

    all_data = list(range(1, 11))
    print(f"    总数据: {all_data}")

    # 使用海象运算符处理批次
    offset = 0
    batch_num = 1
    while batch := get_batch(all_data[offset : offset + 3]):
        print(f"    批次 {batch_num}: {batch}")
        offset += 3
        batch_num += 1
        if offset >= len(all_data):
            break

    # 示例15：配置验证
    print("\n  配置验证:")

    config_dict = {
        "database_url": "postgresql://localhost/db",
        "max_connections": 100,
        "timeout": 30,
    }

    # 传统写法
    print("    传统写法:")
    if "database_url" in config_dict:
        url = config_dict["database_url"]
        if url.startswith("postgresql://"):
            print(f"      数据库URL有效: {url}")

    # 海象运算符
    print("    海象运算符:")
    if (url := config_dict.get("database_url")) and url.startswith("postgresql://"):
        print(f"      数据库URL有效: {url}")

    # 示例16：缓存和去重
    print("\n  缓存和去重:")

    values = [2, 3, 2, 4, 3, 5, 2]
    cache = {}
    results = []

    print(f"    输入值: {values}")

    # 使用海象运算符和缓存
    for val in values:
        if (cached := cache.get(val)) is None:
            # 计算并缓存
            result = expensive_computation(val)
            cache[val] = result
            results.append(result)
            print(f"      计算 {val}³ = {result}")
        else:
            # 使用缓存
            results.append(cached)
            print(f"      使用缓存 {val}³ = {cached}")

    print(f"    最终结果: {results}")


def example_caveats():
    """示例17-20：海象运算符的陷阱和注意事项"""
    print("\n" + "=" * 60)
    print("8. 海象运算符的陷阱和注意事项")
    print("=" * 60)

    # 示例17：作用域问题
    print("  作用域示例:")
    x = 10

    # 海象运算符创建的变量在当前作用域
    if (y := x + 5) > 12:
        print(f"    if语句中: y = {y}")

    print(f"    if语句外: y = {y}  (变量仍然可用)")

    # 示例18：与列表推导式的作用域
    print("\n  列表推导式中的作用域:")
    nums = [1, 2, 3, 4, 5]

    # 传统写法
    doubled1 = [x * 2 for x in nums]
    # print(x)  # NameError: x未定义（在某些Python版本中）

    # 海象运算符
    doubled2 = [last for n in nums if (last := n * 2) > 4]
    print(f"    结果: {doubled2}")
    print(f"    last变量仍可用: {last}")

    # 示例19：可读性权衡
    print("\n  可读性权衡:")

    # 过度使用海象运算符会降低可读性
    data_complex = [1, 2, 3, 4, 5]

    # 推荐：保持简洁
    result = [z for x in data_complex if (y := x * 2) > 3 for z in [y + 1] if z > 5]
    print(f"    推荐写法: {result}")

    # 示例20：与普通赋值的区别
    print("\n  与普通赋值的区别:")
    print("    普通赋值: x = 5  （语句，不返回值）")
    print("    海象运算符: y := 5  （表达式，返回值）")

    # 普通赋值不能用在表达式中
    # if x = 5:  # SyntaxError

    # 海象运算符可以用在表达式中
    if (z := 5) > 3:
        print(f"    海象运算符可以用在表达式中: z = {z}")


@finfo(
    description="演示Python 3.8海象运算符（:=）的各种用法和最佳实践",
    tags=["walrus", "assignment-expression", "python38", "syntax"],
    difficulty="intermediate",
)
def main():
    example_basic_syntax()
    example_while_loop()
    example_if_statement()
    example_list_comprehension()
    example_dict_set_comprehension()
    example_function_call()
    example_real_world_usage()
    example_caveats()


# ============================================================================
# 知识点总结：
# ============================================================================
#
# 1. **基本语法**：
#    - variable := expression
#    - 在表达式内部赋值并返回值
#    - Python 3.8+ 特性
#
# 2. **核心优势**：
#    - 避免重复计算（特别是昂贵的函数调用）
#    - 减少代码冗余
#    - 提高代码可读性（合理使用时）
#    - 简化常见的编程模式
#
# 3. **常见使用场景**：
#    - while循环：简化循环条件
#    - if语句：条件判断中赋值
#    - 列表推导式：避免重复计算
#    - 字典/集合推导式：复用计算结果
#    - 函数调用：在参数中赋值
#    - 正则表达式：匹配和提取
#    - 文件读取：简化读取循环
#    - 数据验证：减少嵌套层次
#
# 4. **最佳实践**：
#    - 优先考虑可读性，不要过度使用
#    - 在确实能提高代码清晰度的地方使用
#    - 避免在复杂的嵌套表达式中使用
#    - 用于避免重复计算昂贵函数
#    - 用于简化常见的模式（如while循环读取）
#
# 5. **注意事项**：
#    - 变量作用域：海象运算符创建的变量在当前作用域
#    - 可读性权衡：过度使用会降低代码可读性
#    - 与普通赋值的区别：:= 是表达式，= 是语句
#    - 不能用于某些上下文（如类属性定义）
#
# 6. **性能考虑**：
#    - 减少函数调用次数，提高性能
#    - 特别适用于昂贵的计算或I/O操作
#    - 在循环和推导式中效果明显
#
# 7. **与其他特性的结合**：
#    - 与推导式结合：避免重复计算
#    - 与正则表达式结合：简化匹配逻辑
#    - 与字典操作结合：减少get()调用
#    - 与文件操作结合：简化读取循环


if __name__ == "__main__":
    main()
