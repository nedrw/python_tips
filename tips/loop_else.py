"""
循环的else子句 - Python中一个强大但常被忽略的特性

循环else机制：
- for和while循环都可以有一个else子句
- else子句在循环**正常完成**（未被break打断）时执行
- 如果循环被break打断，else子句不会执行
"""

from tips import finfo

# ============================================================================
# 辅助函数（模块级别）
# ============================================================================


def search_element(items, target):
    """搜索元素，找到返回索引，未找到返回-1"""
    for index, item in enumerate(items):
        if item == target:
            print(f"  找到目标 '{target}' 在索引 {index}")
            return index
    else:
        # 只有当循环完整执行完毕（未找到目标）时才执行
        print(f"  未找到目标 '{target}'")
        return -1


def validate_all_positive(numbers):
    """验证所有数字是否为正数"""
    for num in numbers:
        if num <= 0:
            print(f"  ✗ 发现非正数: {num}")
            break
    else:
        # 只有当所有元素都是正数时才执行
        print(f"  ✓ 所有数字都是正数: {numbers}")


def is_prime(n):
    """判断一个数是否为素数"""
    if n < 2:
        return False

    # 检查从2到sqrt(n)的所有数
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            # 找到因数，不是素数
            print(f"  {n} = {i} × {n // i}，不是素数")
            return False
    else:
        # 循环完整执行，未找到因数，是素数
        print(f"  ✓ {n} 是素数")
        return True


def try_connect_with_retry(max_retries=3):
    """模拟带重试的连接操作"""
    attempt = 0
    while attempt < max_retries:
        attempt += 1
        print(f"  尝试连接... (第{attempt}次]")

        # 模拟连接成功（这里简化为第3次成功）
        if attempt == 3:
            print("  ✓ 连接成功！")
            break
    else:
        # 所有重试都失败
        print(f"  ✗ 连接失败，已达最大重试次数 {max_retries}")


# ============================================================================
# 示例函数
# ============================================================================


def example_for_loop_else_normal():
    """示例1：for循环正常完成，else被执行"""
    print("=" * 60)
    print("1. for循环 + else：正常完成时执行else")
    print("=" * 60)

    for i in range(3):
        print(f"  迭代 {i}")
    else:
        print("  ✓ 循环正常完成，执行else子句")


def example_for_loop_else_break():
    """示例2：for循环被break打断，else不执行"""
    print("\n" + "=" * 60)
    print("2. for循环 + else：被break打断时不执行else")
    print("=" * 60)

    for i in range(5):
        print(f"  迭代 {i}")
        if i == 2:
            print("  → 遇到break，跳出循环")
            break
    else:
        print("  这行不会被执行")


def example_while_loop_else():
    """示例3：while循环正常完成"""
    print("\n" + "=" * 60)
    print("3. while循环 + else：正常完成时执行else")
    print("=" * 60)

    count = 0
    while count < 3:
        print(f"  计数 {count}")
        count += 1
    else:
        print("  ✓ while循环正常完成，执行else子句")


def example_search_element():
    """示例4：在列表中搜索元素"""
    print("\n" + "=" * 60)
    print("4. 实际应用：搜索元素")
    print("=" * 60)

    # 测试：找到元素的情况
    print("  搜索存在的元素:")
    search_element(["apple", "banana", "cherry"], "banana")

    # 测试：未找到元素的情况
    print("\n  搜索不存在的元素:")
    search_element(["apple", "banana", "cherry"], "orange")


def example_validate_elements():
    """示例5：验证所有元素是否满足条件"""
    print("\n" + "=" * 60)
    print("5. 实际应用：验证所有元素")
    print("=" * 60)

    # 测试：所有正数
    print("  验证 [1, 2, 3, 4, 5]:")
    validate_all_positive([1, 2, 3, 4, 5])

    # 测试：包含非正数
    print("\n  验证 [1, 2, -1, 4, 5]:")
    validate_all_positive([1, 2, -1, 4, 5])


def example_find_prime():
    """示例6：使用循环else判断素数"""
    print("\n" + "=" * 60)
    print("6. 实际应用：查找素数")
    print("=" * 60)

    # 测试几个数字
    test_numbers = [2, 7, 15, 17, 21]
    for num in test_numbers:
        is_prime(num)


def example_retry_mechanism():
    """示例7：带重试次数限制的操作"""
    print("\n" + "=" * 60)
    print("7. while循环 + else：重试机制")
    print("=" * 60)

    # 测试重试机制
    try_connect_with_retry()


def example_nested_loop():
    """示例8：嵌套循环中的else"""
    print("\n" + "=" * 60)
    print("8. 嵌套循环中的else")
    print("=" * 60)

    print("  查找二维列表中的目标值:")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    target = 5

    for row_idx, row in enumerate(matrix):
        for col_idx, value in enumerate(row):
            if value == target:
                print(f"  找到 {target} 在位置 ({row_idx}, {col_idx})")
                break
        else:
            # 内层循环完整执行，未找到目标
            print(f"  第 {row_idx} 行未找到目标")
            continue  # 继续下一行

        # 如果内层循环被break打断，会执行到这里
        break  # 跳出外层循环
    else:
        # 外层循环完整执行，所有行都未找到
        print(f"  未找到目标 {target}")


@finfo(
    description="演示Python循环的else子句机制，包括for/while循环与break的交互",
    tags=["loop", "control-flow", "else", "break"],
    difficulty="intermediate",
)
def main():
    example_for_loop_else_normal()
    example_for_loop_else_break()
    example_while_loop_else()
    example_search_element()
    example_validate_elements()
    example_find_prime()
    example_retry_mechanism()
    example_nested_loop()


# ============================================================================
# 知识点总结：
# ============================================================================
#
# 1. **基本语法**：
#    for item in iterable:
#        # 循环体
#        if condition:
#            break
#    else:
#        # 循环正常完成时执行
#
# 2. **执行规则**：
#    - 循环正常完成（没有被break打断）→ 执行else
#    - 循环被break打断 → 不执行else
#    - 循环为空（如range(0)）→ 执行else
#    - continue不影响else的执行
#
# 3. **常见应用场景**：
#    - 搜索操作：未找到时的默认处理
#    - 验证操作：所有元素都满足条件时执行
#    - 重试机制：达到最大重试次数后的处理
#    - 数学计算：如判断素数
#
# 4. **替代方案对比**：
#    - 使用标志变量
#    - 使用函数和return
#    - 使用异常处理
#    - 循环else通常更简洁直观
#
# 5. **注意事项**：
#    - else子句容易与if-else混淆，要记住这里的else是"没有break时执行"
#    - 可以理解为"如果没有break，就执行else"
#    - 在嵌套循环中，else只与最近的循环配对

if __name__ == "__main__":
    main()
