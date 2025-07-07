import itertools

from tips import finfo


@finfo
def example_chain():
    # 将多个可迭代对象连接起来
    result = list(itertools.chain([1, 2], [3, 4], [5]))
    print("chain result:", result)


@finfo
def example_count():
    # 生成从 start 开始的连续整数（结合其他函数使用）
    for i in itertools.islice(itertools.count(10), 5):
        print("count item:", i)


@finfo
def example_cycle():
    # 循环遍历一个可迭代对象
    for i in itertools.islice(itertools.cycle([1, 2, 3]), 7):
        print("cycle item:", i)


@finfo
def example_repeat():
    # 重复某个元素 n 次
    result = list(itertools.repeat(7, 4))
    print("repeat result:", result)


@finfo
def example_combinations():
    # 获取所有长度为 2 的组合
    result = list(itertools.combinations([1, 2, 3], 2))
    print("combinations result:", result)


@finfo
def example_permutations():
    # 获取所有长度为 2 的排列
    result = list(itertools.permutations([1, 2, 3], 2))
    print("permutations result:", result)


@finfo
def example_product():
    # 笛卡尔积
    result = list(itertools.product([1, 2], [3, 4]))
    print("product result:", result)


@finfo
def example_groupby():
    # 根据 key 函数对序列进行分组
    data = [("a", 1), ("a", 2), ("b", 3), ("b", 4)]
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        print(f"groupby key: {key}, values: {list(group)}")


@finfo
def example_islice():
    # 类似切片操作，适用于迭代器
    result = list(itertools.islice([10, 20, 30, 40], 1, None, 2))
    print("islice result:", result)


@finfo
def example_tee():
    # 创建多个独立的迭代器副本
    iter1, iter2 = itertools.tee([1, 2, 3], 2)
    print("tee first copy:", list(iter1))
    print("tee second copy:", list(iter2))


@finfo
def main():
    example_chain()
    example_count()
    example_cycle()
    example_repeat()
    example_combinations()
    example_permutations()
    example_product()
    example_groupby()
    example_islice()
    example_tee()


if __name__ == "__main__":
    main()
