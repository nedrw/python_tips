"""
链式运算符 - Python中优雅且高效的连续操作语法

链式运算符特性：
- 链式比较：a < x < b（更简洁，更高效，x只求值一次）
- 链式赋值：x = y = z = value（多个变量同时赋值）
- 链式调用：obj.method1().method2().method3()（流畅接口模式）
- 链式布尔运算：连续的逻辑判断
"""

from tips import finfo

# ============================================================================
# 辅助类和函数（模块级别）
# ============================================================================


class StringBuilder:
    """支持链式调用的字符串构建器"""

    def __init__(self, initial=""):
        self.value = initial

    def append(self, text):
        self.value += text
        return self  # 返回self以支持链式调用

    def upper(self):
        self.value = self.value.upper()
        return self

    def prefix(self, text):
        self.value = text + self.value
        return self

    def __str__(self):
        return self.value


def get_value():
    """模拟一个昂贵的函数调用"""
    print("    [函数被调用]", end=" ")
    return 5


def check_positive(n):
    """检查数字是否为正数"""
    print(f"    [检查 {n} > 0]", end=" ")
    return n > 0


def validate_age(age):
    """验证年龄范围"""
    if 0 <= age <= 120:
        print(f"  ✓ 年龄 {age} 有效")
        return True
    else:
        print(f"  ✗ 年龄 {age} 无效")
        return False


def get_grade(score):
    """根据分数返回等级"""
    if 90 <= score <= 100:
        return "A"
    elif 80 <= score < 90:
        return "B"
    elif 70 <= score < 80:
        return "C"
    elif 60 <= score < 70:
        return "D"
    else:
        return "F"


def is_workday(check_date):
    """检查日期是否在工作日范围内（周一到周五）"""
    # weekday(): 0=周一, 6=周日
    if 0 <= check_date.weekday() <= 4:
        return True
    return False


# ============================================================================
# 示例函数
# ============================================================================


def example_chained_comparison():
    """示例1-3：链式比较运算符基础"""
    print("=" * 60)
    print("1. 链式比较运算符")
    print("=" * 60)

    # 示例1：基本链式比较
    x = 5
    print(f"  x = {x}")
    result = 1 < x < 10
    print(f"  1 < x < 10  → {result}")

    result = 1 < x < 3
    print(f"  1 < x < 3   → {result}")

    # 示例2：多条件链式比较
    y = 15
    print(f"\n  y = {y}")
    result = 10 < y < 20
    print(f"  10 < y < 20      → {result}")

    result = 10 < y <= 15
    print(f"  10 < y <= 15     → {result}")

    # 示例3：不等式链式比较
    z = 5
    print(f"\n  z = {z}")
    result = 0 < z < 10
    print(f"  0 < z < 10       → {result}")

    result = 3 < z < 7
    print(f"  3 < z < 7        → {result}")


def example_performance_comparison():
    """示例4-5：链式比较 vs 传统比较"""
    print("\n" + "=" * 60)
    print("2. 链式比较 vs 传统比较")
    print("=" * 60)

    # 示例4：性能对比 - 链式比较更高效
    print("  传统写法 vs 链式写法:")
    value = 50

    # 传统写法：value会被求值两次
    result1 = value > 0 and value < 100
    print(f"    value > 0 and value < 100  → {result1}")

    # 链式写法：value只求值一次，更高效
    result2 = 0 < value < 100
    print(f"    0 < value < 100            → {result2}")

    # 示例5：带函数调用的链式比较
    print("\n  传统写法（函数调用两次）:")
    result = get_value() > 0 and get_value() < 10
    print(f"→ {result}")

    print("  链式写法（函数只调用一次）:")
    result = 0 < get_value() < 10
    print(f"→ {result}")


def example_equivalent_forms():
    """示例6-7：链式比较的等价形式"""
    print("\n" + "=" * 60)
    print("3. 链式比较的等价形式")
    print("=" * 60)

    # 示例6：理解链式比较的展开
    a, b, c = 1, 2, 3
    print(f"  a={a}, b={b}, c={c}")
    print(f"  a < b < c  → {a < b < c}")
    print(f"  等价于: a < b and b < c")

    # 示例7：混合运算符
    x_val = 5
    print(f"\n  x = {x_val}")
    result = 0 <= x_val < 10
    print(f"  0 <= x < 10   → {result}")

    result = 0 < x_val <= 10
    print(f"  0 < x <= 10   → {result}")

    result = 3 < x_val != 10
    print(f"  3 < x != 10   → {result}")


def example_chained_assignment():
    """示例8-9：链式赋值"""
    print("\n" + "=" * 60)
    print("4. 链式赋值")
    print("=" * 60)

    # 示例8：基本链式赋值
    a = b = c = 10
    print(f"  a = b = c = 10")
    print(f"  a = {a}, b = {b}, c = {c}")

    # 示例9：链式赋值与可变对象（注意陷阱）
    print("\n  链式赋值的陷阱（可变对象）:")
    x = y = []
    print(f"  x = y = []")
    print(f"  x is y: {x is y}")  # True - 它们指向同一个对象

    x.append(1)
    print(f"  执行 x.append(1) 后:")
    print(f"  x = {x}, y = {y}")  # x和y都被修改了！

    # 正确的做法：独立创建
    print("\n  正确做法（独立创建）:")
    x = []
    y = []
    print(f"  x = [], y = []")
    print(f"  x is y: {x is y}")  # False - 它们是不同的对象


def example_fluent_interface():
    """示例10-12：链式方法调用（流畅接口）"""
    print("\n" + "=" * 60)
    print("5. 链式方法调用（流畅接口）")
    print("=" * 60)

    # 示例10：字符串的链式方法调用
    text = "  hello world  "
    result = text.strip().upper().replace(" ", "_")
    print(f"  原始字符串: '{text}'")
    print(f"  链式调用: strip().upper().replace(' ', '_')")
    print(f"  结果: '{result}'")

    # 示例11：列表的链式方法调用
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    # 注意：list.sort()返回None，不能链式调用
    # 但可以使用sorted()
    result = sorted([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"\n  原始列表: {numbers}")
    print(f"  sorted(numbers): {result}")

    # 示例12：自定义类的流畅接口
    builder = StringBuilder()
    result = builder.append("Hello").append(" ").append("World").upper().prefix(">>> ")
    print(f"\n  StringBuilder链式调用:")
    print(f"  .append('Hello').append(' ').append('World').upper().prefix('>>> ')")
    print(f"  结果: '{result}'")


def example_boolean_operations():
    """示例13-15：链式布尔运算"""
    print("\n" + "=" * 60)
    print("6. 链式布尔运算")
    print("=" * 60)

    # 示例13：链式布尔运算
    a_bool, b_bool, c_bool = True, False, True
    print(f"  a={a_bool}, b={b_bool}, c={c_bool}")
    result = a_bool and b_bool and c_bool
    print(f"  a and b and c  → {result}")

    result = a_bool or b_bool or c_bool
    print(f"  a or b or c    → {result}")

    # 示例14：结合比较和布尔运算
    x_num = 5
    y_num = 10
    result = 0 < x_num < y_num < 20
    print(f"\n  x={x_num}, y={y_num}")
    print(f"  0 < x < y < 20  → {result}")

    # 示例15：短路求值
    print("\n  短路求值演示:")
    print("  check_positive(1) and check_positive(0) and check_positive(2):")
    result = check_positive(1) and check_positive(0) and check_positive(2)
    print(f"→ {result}")


def example_real_world_usage():
    """示例16-18：实际应用场景"""
    print("\n" + "=" * 60)
    print("7. 实际应用场景")
    print("=" * 60)

    # 示例16：范围验证
    print("  年龄验证:")
    validate_age(25)
    validate_age(-5)
    validate_age(150)

    # 示例17：区间判断
    print("\n  成绩等级:")
    for score in [95, 85, 75, 65, 55]:
        grade = get_grade(score)
        print(f"  分数 {score:3d} → 等级 {grade}")

    # 示例18：日期范围检查
    from datetime import date

    print("\n  工作日检查:")
    test_date = date(2024, 1, 8)  # 周一
    print(f"  {test_date} 是工作日: {is_workday(test_date)}")

    test_date = date(2024, 1, 7)  # 周日
    print(f"  {test_date} 是工作日: {is_workday(test_date)}")


def example_edge_cases():
    """示例19-21：链式比较的边界情况"""
    print("\n" + "=" * 60)
    print("8. 链式比较的边界情况")
    print("=" * 60)

    # 示例19：相同运算符的链式比较
    a_val = 5
    print(f"  a = {a_val}")
    result = a_val == a_val == a_val
    print(f"  a == a == a  → {result}")

    # 示例20：不同类型比较
    print("\n  不同类型的比较:")
    print(f"  1 == 1.0 == True  → {1 == 1.0 == True}")
    print(f"  1 is 1 is 1        → {1 is 1 is 1}")  # 小整数缓存

    # 示例21：空值检查链
    value = None
    print(f"\n  value = {value}")
    # 安全的None检查
    if value is not None and 0 < value < 10:
        print("  值在范围内")
    else:
        print("  值为None或不在范围内")


@finfo(
    description="演示Python链式运算符的各种用法，包括比较、赋值、方法调用和布尔运算",
    tags=["operator", "comparison", "chaining", "fluent-interface"],
    difficulty="intermediate",
)
def main():
    example_chained_comparison()
    example_performance_comparison()
    example_equivalent_forms()
    example_chained_assignment()
    example_fluent_interface()
    example_boolean_operations()
    example_real_world_usage()
    example_edge_cases()


# ============================================================================
# 知识点总结：
# ============================================================================
#
# 1. **链式比较**：
#    - 语法：a < x < b（等价于 a < x and x < b）
#    - 优势：更简洁、更易读、x只求值一次（性能更好）
#    - 支持的运算符：<, <=, >, >=, ==, !=, is, is not, in, not in
#
# 2. **链式赋值**：
#    - 语法：x = y = z = value
#    - 注意：可变对象会共享引用（x is y 返回 True）
#    - 推荐：对可变对象独立创建，避免意外共享
#
# 3. **链式方法调用**：
#    - 语法：obj.method1().method2().method3()
#    - 要求：每个方法返回对象本身（self）或新对象
#    - 应用：流畅接口模式、Builder模式
#
# 4. **链式布尔运算**：
#    - 语法：a and b and c 或 a or b or c
#    - 特性：短路求值，提前终止
#    - 注意：返回的是最后一个求值的元素，不一定是布尔值
#
# 5. **性能优势**：
#    - 链式比较比传统比较更高效（减少求值次数）
#    - 特别适用于涉及函数调用的比较
#
# 6. **常见陷阱**：
#    - 链式赋值可变对象会共享引用
#    - 链式比较中的is/is not要小心使用
#    - 链式调用时要确保方法返回正确的对象
#
# 7. **最佳实践**：
#    - 优先使用链式比较代替传统比较
#    - 对可变对象避免使用链式赋值
#    - 设计类时考虑流畅接口模式
#    - 结合条件判断使用链式比较提高可读性


if __name__ == "__main__":
    main()
